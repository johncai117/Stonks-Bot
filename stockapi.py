import yfinance as yf
import numpy as np

class StockInfo():
    def __init__(self,ticker):
        self.tick = yf.Ticker(ticker[0])
        self.hist = self.tick.history(period="5d")
        #print(self.hist)
    
    def latest_price(self):
        close = round(float(self.hist["Close"][-1]),3)
        latest_date = self.hist.index.values[-1]
        latest_date = np.datetime_as_string(latest_date, unit='D') ##convert to datetime
        
        return close, latest_date

#instance = StockInfo("AAPL")

#print(instance.latest_price())