from backtest import backtest
import pandas as pd
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
# from pyinstrument import Profiler

btc = pd.read_csv("small.csv")
btc = btc.dropna()
btc = btc.drop(["Volume(Currency)", "WPrice"], axis = 1)

bt = backtest()
bt.addOHLCV(btc)

bt.next()
# op = bt.open(0, bt.balance/2)
# op = bt.open(0, bt.balance)
# op = bt.open(0, 3
for i in tqdm(range(len(btc))):
    if bt.balance > 0:
        bt.open(0,1)
    returnCode = bt.next()
    if returnCode is False:
        break

print(bt.options["Open"])
print(bt.options["Closed"])
print(bt.balance)

plt.plot(bt.logs["investmentValue"].keys(), bt.logs["investmentValue"].values())
plt.show()
