import yfinance as yf
import datetime

class Broker():
    def __init__(self, file_name=None):
        if file_name is not None:
            file = open(file_name, "r")
            data = file.read()
            file.close()

            self.trading_holidays = data.split(",")
            for i in range(len(self.trading_holidays)):
                pre_process_date = self.trading_holidays[i].strip("'\n'")
                self.trading_holidays[i] = datetime.datetime.strptime(pre_process_date, '%d-%m-%Y').date()

    def is_trading_day(self, cur_day):
        if cur_day in self.trading_holidays:
            return False
        else:
            return True

    def get_stock_price(self, ticker, start, end):
        stock_data = yf.download(ticker, start=start, end=end)
        return stock_data.index[0].date(), stock_data.iloc[0]['Close']
    
    def check_trading_holidays(self, cur_day):
        try:
            if cur_day.weekday() <= 4:
                self.get_stock_price("^HSI", cur_day, cur_day + datetime.timedelta(days=1))
                return True
            return False
        except:
            return False