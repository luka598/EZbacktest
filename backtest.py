from numpy import column_stack
import pandas as pd

class backtest():
    def __init__(self, ohlcv):
        self.ohlcvAll = ohlcv
        self.backdata = 100
        self.maxOrderLifetime = 1
        self.uninvestedBalance = 100
        self.orders = pd.DataFrame(columns = ["Status", "Type", "Price", "SL", "TP"])
        self.positions = pd.DataFrame(columns=["Open", "Type", "OpenValue", "CloseValue", "Profit", "SL", "TP"])
        self.iteration = 0

    def next(self):
        self.shift()
        self.fillOrders()
        pass

    def shift(self):
        self.ohlcv = self.ohlcvAll[self.iteration:self.backdata+self.iteration]
        self.iteration += 1
        return

    def fillOrders(self):
        for order in self.orders:
            if self.uninvestedBalance < order["Price"]:

            self.positions.append({
                "Open": True,
                "Type": order["Type"],
                "OpenValue": order["Price"],
                "CloseValue": 0,
                "Profit": 0,
                "SL": order["SL"],
                "TP": order["TP"]
            })
            self.uninvestedBalance -= self.ohlcv[-1]["Open"]
        return

    def calculatePositionProfit(self):


    def balance(self):
        pass

    def getPositions():
        pass

    def buy():
        pass

    def sell():
        pass
