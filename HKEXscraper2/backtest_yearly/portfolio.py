import pandas as pd
import numpy as np
import datetime
import time
import yfinance as yf

class Portfolio:
    
    def __init__(self, init_cap, size, bmark_score, report, score_2017, score_2018, score_2019, score_2020, score_2021, score_2022):
        self.size = size # 10
        self.bmark_score = bmark_score # 30
        self.ESG_report = report
        self.report = report
        self.score_2017 = score_2017
        self.score_2018 = score_2018
        self.score_2019 = score_2019
        self.score_2020 = score_2020
        self.score_2021 = score_2021
        self.score_2022 = score_2022
        self.cur_day = None

        # Stock Account
        self.init_cap = init_cap
        self.balance = init_cap # 100,000,000
        self.portfolios = []
        self.buy_orders = []
        self.sell_orders = []
        self.transactions = []
        self.daily_pls = []

    def get_balance(self):
        return self.balance
    
    def get_size(self):
        return self.size

    def get_bmark_score(self):
        return self.bmark_score
    
    def get_portfolios(self):
        return self.portfolios
    
    def get_transactions(self):
        return self.transactions
    
    def get_daily_pls(self):
        return self.daily_pls
    
    def get_stock_data(self, ticker, start, end):
        stock_data = yf.download(ticker, start=start, end=end)
        return stock_data.index[0].date(), stock_data.iloc[0]['Close']


    def strategy(self):
        start_date = datetime.datetime(2018, 1, 1).date()
        end_date = datetime.datetime(2018,12,31).date()
        self.cur_day = start_date
        report_cols = self.report.columns.values.tolist()
        while self.cur_day != end_date:
            for index, row in self.report.iterrows():
                stock_code = row['stock_code'][1:]
                for col in report_cols[1:]:
                    if row[col].date() == self.cur_day:
                        year = self.cur_day.year
                        if year == 2017:
                            try:
                                score = self.score_2017.loc[self.score_2017['file_name'] == stock_code]['positive'].values[0]
                                # print(stock_code, row[col].date(), year, score)
                                self.longShort(stock_code, row[col].date(), score)
                            except:
                                pass
                        if year == 2018:
                            try:
                                score = self.score_2018.loc[self.score_2018['file_name'] == stock_code]['positive'].values[0]
                                # print(stock_code, row[col].date(), year, score)
                                self.longShort(stock_code, row[col].date(), score)
                            except:
                                pass
                                # print("Stock Code " + stock_code + " Not Found in year " + str(year))
                        # if year == 2018:
                        #     try:
                        #         score = self.score_2018.loc[self.score_2018['file_name'] == stock_code]['positive'].values[0]
                        #         print(stock_code, row[col].date(), year, score)
                        #     except:
                        #         pass
                                # print("Stock Code " + stock_code + " Not Found in year " + str(year))

            rm_portoflio = []
            rm_buy_order = []
            rm_sell_order = []

            for portfolio in self.portfolios:
                if portfolio["sell_date"] == self.cur_day:
                    rm_portoflio.append(portfolio)
            
            for buy_order in self.buy_orders:
                if buy_order["date"] == self.cur_day:
                    self.executeOrder(buy_order)
                    rm_buy_order.append(buy_order)

            for sell_order in self.sell_orders:
                if sell_order["date"] == self.cur_day:
                    self.executeOrder(sell_order)
                    rm_sell_order.append(sell_order)
            
            self.portfolios = [portfolio for portfolio in self.portfolios if portfolio not in rm_portoflio]
            self.buy_orders = [buy_order for buy_order in self.buy_orders if buy_order not in rm_buy_order]
            self.sell_orders = [sell_order for sell_order in self.sell_orders if sell_order not in rm_sell_order]

            self.cal_daily_pl()

            self.cur_day += datetime.timedelta(days=1)
            # print(self.cur_day)

    def long(self, ticker, buy_date, buy_share_price, sell_date, sell_share_price):
        if len(self.portfolios) < self.size:
            divisor = (self.size - len(self.portfolios))
            buy_amount = int((self.balance / divisor) / buy_share_price)

            # attach order
            buy_order = {"ticker": ticker, "date": buy_date, "amount": buy_amount * buy_share_price, "buy": True}
            sell_order = {"ticker": ticker, "date": sell_date, "amount": buy_amount * sell_share_price, "buy": False}
            self.buy_orders.append(buy_order)
            self.sell_orders.append(sell_order)

            # add to portfolio
            new_portfolio = {"ticker": ticker, "buy_date": buy_date, "sell_date": sell_date, "buy_amount": buy_amount, "long": True}
            self.portfolios.append(new_portfolio)
            
    def cal_daily_pl(self):
        try:
            cash_balance = self.balance
            stock_balance = 0
            for portfolio in self.portfolios:
                if portfolio["long"] is True:
                    if portfolio["buy_date"] <= self.cur_day:
                        date, share_price = self.get_stock_data(portfolio["ticker"], self.cur_day, self.cur_day + datetime.timedelta(days=1))
                        stock_balance += share_price * portfolio["buy_amount"]
            daily_pl = {"date": self.cur_day, "pl": (cash_balance + stock_balance) - self.init_cap, "balance": cash_balance + stock_balance}
            self.daily_pls.append(daily_pl)
        except:
            print(self.cur_day.strftime("%d-%m-%Y") + " is holiday")
            daily_pl = {"date": self.cur_day, "pl": self.daily_pls[-1]["pl"], "balance": self.daily_pls[-1]['balance'] }
            #daily_pl = self.daily_pls[-1]
            #daily_pl["date"] = self.cur_day
            # print(daily_pl)
            self.daily_pls.append(daily_pl)
            # print(self.daily_pls[-1])
            # print(self.daily_pls[-2])
    
    def executeOrder(self, order):
        if order["buy"] is True:
            self.balance -= order["amount"]
            new_transaction = {"ticker": order["ticker"], "date": order["date"], "amount": "-" + str(order["amount"]), "remaining_capital": str(self.balance)}
        else:
            self.balance += order["amount"]
            new_transaction =  {"ticker": order["ticker"], "date": order["date"], "amount": "+" + str(order["amount"]), "remaining_capital": str(self.balance)}
        self.transactions.append(new_transaction)

    def longShort(self, ticker, date, score):
        if score >= self.bmark_score:
            # long
            # get buy_date, sell_date, buy_share_price, sell_share_price
            print(ticker + " score of " + str(score) + " is greater than " + str(self.bmark_score))
            #print(date, end_date)
            buy_date, buy_share_price = self.get_stock_data(ticker, date, date + datetime.timedelta(days=7))
            print(buy_date, buy_share_price)
            sell_date, sell_share_price = self.get_stock_data(ticker, buy_date + datetime.timedelta(days=31), buy_date + datetime.timedelta(days=38))
            
            self.long(ticker, buy_date, buy_share_price, sell_date, sell_share_price)
        else:
            # short
            print(ticker + " score of " + str(score) + " is not greater than " + str(self.bmark_score))
