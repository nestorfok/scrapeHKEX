import yfinance as yf
import datetime

class Broker():
    def __init__(self):
        pass

    def is_trading_day(self, cur_day):
        try:
            if cur_day.weekday() <= 4:
                self.get_stock_price("^HSI", cur_day, cur_day + datetime.timedelta(days=1))
                return True
            return False
        except:
            return False

    def get_stock_price(self, ticker, start, end):
        stock_data = yf.download(ticker, start=start, end=end)
        return stock_data.index[0].date(), stock_data.iloc[0]['Close']