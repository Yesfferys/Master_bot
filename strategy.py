
from talib import EMA, RSI, MACD
import pandas_ta as ta

class indicators:

    def __init__(self,data):
        self.close=data.get("Close")
        self.low=data.get("Low")
        self.high=data.get("Higt")
        
    def ema(self):
        return EMA(
            self.close,
            timeperiod=15
        ).iloc[-1]

    def rsi(self,timeperiod:int=14):
        return RSI(
           self.close,
            timeperiod=timeperiod
        ).iloc[-1]

    def macd(self,fastperiod:int=12,slowperiod:int=26,signalperiod:int=9):
        _macd, macdsignal, _ = MACD(
            self.close,
            fastperiod,
            slowperiod,
            signalperiod
        )
        return _macd.iloc[-1], macdsignal.iloc[-1]

    def adx(self):
        return ta.adx(self.high,self.low,self.close)