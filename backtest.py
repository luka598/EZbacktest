from collections import deque
import time
import uuid
import pandas as pd

class option():
    '''
    Return codes:
    0: Finished,
    1: ,
    2:
    '''
    def __init__(self):
        self.uuid = uuid.uuid4().hex
        self.active = False
        self.status = -1 # 0: Open, 1: Close
        self.direction = -1 # 0: Up(Long), 1: Down(Short)
        self.openPrice = -1
        self.openTime = -1
        self.closePrice = -1
        self.closeTime = -1
        self.currentPrice = -1
        self.currentTime = -1
        self.originalValue = -1
        self.currentValue = -1
        self.lifetime = -1
        self.change = -1
        self.profitP = -1
        self.tp = 0
        self.sl = 0

    def update(self, cache):
        if self.active is False and self.status == 1:
            return 0

        self.currentPrice = cache[0]
        self.currentTime = cache[1]

        # self.currentPrice = ohlcv["Open"].iloc[self.openTime+self.lifetime]
        # self.currentTime = ohlcv["index"].iloc[self.openTime+self.lifetime]

        # self.currentPrice = ohlcv["Open"].tail(1).item()
        # self.currentTime = ohlcv["index"].tail(1).item()

        if self.active:
            if self.status == 0:
                self.openPrice = self.currentPrice
                self.openTime = self.currentTime
                self.active = False
            elif self.status == 1:
                self.closePrice = self.currentPrice
                self.closeTime = self.currentTime
                self.active = False

        self.change = self.currentPrice/self.openPrice-1

        if self.direction == 0:
            self.profitP = self.change
        elif self.direction == 1:
            self.profitP = -self.change

        self.currentValue = self.originalValue*(self.change+1)

        if self.status != 1:
            if self.profitP >= self.tp:
                self.close()
            if self.profitP <= self.sl:
                self.close()

        self.lifetime += 1
        return 1

    def open(self, direction, value, tp, sl):
        self.active = True
        self.status = 0
        self.direction = direction
        self.tp = tp
        self.sl = sl
        self.originalValue = value
        self.lifetime = 0
        return

    def close(self):
        self.active = True
        self.status = 1
        return

class backtest():
    def __init__(self):
        self.active = True # 0: NormalExecution, 1: Stopping, 2: Stopped

        self.ohlcvFull = pd.DataFrame()
        self.ohlcv = pd.DataFrame()
        self.dataWindow = 100
        self.balance = 100
        self.investmentValue = 0
        self.iteration = 0
        self.dataLenght = 0

        self.openCache = -1
        self.timeCache = -1

        self.logs = {"balance":{},
                     "investmentValue": {}}

        self.options = {
            "Open": {},
            "Closed": {}
        }
        return

    def addOHLCV(self, ohlcv):
        #TODO: Add checks that ohlcv data is valid 
        self.ohlcvFull = ohlcv.reset_index()
        self.dataLenght = len(self.ohlcvFull)
        return

    def updateOHLCV(self):
        if self.iteration >= self.dataLenght - self.dataWindow:
            return 0

        self.ohlcv = self.ohlcvFull.iloc[self.iteration:self.iteration+self.dataWindow] ## pyright: reportOptionalSubscript=false

        if self.ohlcv.empty:
            return 0

        return 1

    def cache(self):
        self.openCache = self.currentPrice = self.ohlcv["Open"].iloc[self.dataWindow-1] #pyright: reportOptionalMemberAccess=false
        self.timeCache = self.iteration+self.dataWindow
        return

    def updateOrders(self):
        self.investmentValue = 0
        closedOptions = []
        for optionUUID in self.options["Open"]:
            returnCode = self.options["Open"][optionUUID].update((self.openCache, self.timeCache))
            if returnCode == 0:
                closedOptions.append(optionUUID)
            else:
                self.investmentValue += self.options["Open"][optionUUID].currentValue
        for optionUUID in closedOptions:
            self.balance += self.options["Open"][optionUUID].currentValue
            self.options["Closed"][optionUUID] = self.options["Open"].pop(optionUUID)
        return

    def next(self):
        if not self.active:
            return False

        returnCode = self.updateOHLCV()

        if returnCode == 0:
            self.stop()
            self.active = False
            return False

        self.cache()
        self.updateOrders()

        self.log()

        self.iteration += 1
        return True

    def log(self):
        self.logs["balance"][self.iteration] = self.balance
        self.logs["investmentValue"][self.iteration] = self.investmentValue
        return

    def stop(self):
        self.closeOrders()
        self.updateOrders()
        self.updateOrders()

    def closeOrders(self):
        for optionUUID in self.options["Open"]:
            self.options["Open"][optionUUID].close()

    def open(self, direction, value, tp = 999, sl = -999):
        op = option()
        op.open(direction, value, tp = tp, sl = sl)
        self.balance -= value
        self.options["Open"][op.uuid] = op
        return op.uuid # pyright: reportGeneralTypeIssues=false

    def close(self, optionUUID):
        op = self.options["Open"][optionUUID]
        op.close()
        return
