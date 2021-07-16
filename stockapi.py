import yfinance as yf
import numpy as np
import pandas as pd

def area_plot(prices, dates, name, chatid ):
    import matplotlib.pyplot as plt
    plt.switch_backend('Agg') 
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(dates, prices)

    import matplotlib.dates as mdates
    myFmt = mdates.DateFormatter('%d %b %y')
    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    ax.set_xlim(dates[0], dates[-1])

    

    min_date = pd.to_datetime(dates[0]).strftime('%d %b %Y') 
    max_date = pd.to_datetime(dates[-1]).strftime('%d %b %Y') 
    plt.title("$"+ name + " Closing Price from " + min_date + " to " + max_date)

    plt.savefig(str(chatid) + "_" + name + '.png')

    return str(chatid) + "_" + name + '.png'
    

    

class StockInfo():
    def __init__(self,ticker, chat_id = "000"):
        if isinstance(ticker, str):
            self.tick = yf.Ticker(ticker)
        else:
            self.tick = yf.Ticker(ticker[0])
            assert self.tick.ticker == ticker[0], "Ticker Name Unknown"
        self.hist = self.tick.history(period="5d")
        self.chat_id = chat_id
    
    def latest_price(self):
        close = round(float(self.hist["Close"][-1]),4)
        latest_date = self.hist.index.values[-1]
        latest_date = pd.to_datetime(latest_date).strftime('%d %b %Y')
        
        return str(close), latest_date
    
    def five_day(self):
        close = [round(float(x),4) for x in self.hist["Close"]]
        latest_dates = self.hist.index.values
        
        return 
    
    def days_past(self, num_days = 30):
        self.hist = self.tick.history(period=str(num_days)+"d")
        close = [round(float(x),4) for x in self.hist["Close"]]
        latest_dates = self.hist.index.values
        return area_plot(close, latest_dates, str(self.tick.ticker), self.chat_id)


if __name__ == "__main__":
    instance = StockInfo(["KO"])
    print(instance.latest_price())
    print(instance.days_past(100))