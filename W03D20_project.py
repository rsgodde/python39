import talib as ta
import numpy as np
from datetime import date
from datetime import timedelta
from nsepy import get_history

def sma_backtest(stock, period1,period2):
        stock = get_history(symbol=stock, start=date.today()-timedelta(days=300), end=date.today())
        sma10=ta.SMA(stock["Close"],timeperiod=period1)
        sma21=ta.SMA(stock["Close"],timeperiod=period2)
        i=0
        buy=0
        sell=0
        nos=0
        long=0
        short=0
        while i < len(sma10):
                if sma10[i] == "nan" :
                        continue
                if sma21[i] == "nan" :
                        continue
                if sma10[i]>sma21[i]:
                        if long==0:
                                long=1
                                short=0
                                buy=buy+1
                                print(stock["Close"][i],sma10[i],sma21[i],"Long")
                else:
                        if sma10[i]<sma21[i]:
                                if short==0:
                                        long=0
                                        short=1
                                        sell=sell+1
                                        print(stock["Close"][i],sma10[i],sma21[i],"Short")
                        else:
                                print(stock["Close"][i],sma10[i],sma21[i],"NOS")
                                nos=nos+1

                i=i+1

        print("buy =",buy,",sell =",sell,",No Signal =",nos)
        return 0



smg=sma_backtest("SBIN",10,21)

