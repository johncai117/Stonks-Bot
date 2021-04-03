import yfinance as yf
import numpy as np
import pandas as pd

class StockInfo():
    def __init__(self,ticker):
        if isinstance(ticker, str):
            self.tick = yf.Ticker(ticker)
        else:
            self.tick = yf.Ticker(ticker[0])
            assert self.tick.ticker == ticker[0], "Ticker Name Unknown"            
        self.hist = self.tick.history(period="5d")
        #print(self.hist)
    
    def latest_price(self):
        close = round(float(self.hist["Close"][-1]),4)
        latest_date = self.hist.index.values[-1]
        latest_date = pd.to_datetime(latest_date).strftime('%d %b %Y')
        
        return str(close), latest_date


if __name__ == "__main__":
    instance = StockInfo(["AAPL"])
    print(instance.latest_price())