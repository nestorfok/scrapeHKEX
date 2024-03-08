import pandas as pd
import numpy as np
import datetime
import time
import yfinance as yf

class portfolio:
    
    def __init__(self, init_cap, size, bmark_score, report, score_2017, score_2018, score_2019, score_2020, score_2021, score_2022):
        self.size = size # 0.1
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
        self.balance = init_cap # 100,000,000
        self.portfolios = []
        self.buy_orders = []
        self.sell_orders = []
        self.transactions = []

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
    
    def get_stock_data(self, ticket, start, end):
        stock_data = yf.download(ticket, start=start, end=end)
        return stock_data['Date'].values[0], stock_data['Close'].values[0]


    def strategy(self, start_date, end_date):
        start_date = datetime.datetime(2017, 4, 5).date()
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
                                self.long(stock_code, row[col].date(), score)
                            except:
                                pass
                                # print("Stock Code " + stock_code + " Not Found in year " + str(year))
                        if year == 2018:
                            try:
                                score = self.score_2018.loc[self.score_2018['file_name'] == stock_code]['positive'].values[0]
                                print(stock_code, row[col].date(), year, score)
                            except:
                                pass
                                # print("Stock Code " + stock_code + " Not Found in year " + str(year))
                
                for index in range(len(self.portfolios)):
                    if self.portfolios[index]['date'] == start_date:
                        self.empty(index)
        
            self.cur_day += datetime.timedelta(days=1)
            time.sleep(0.0005)

    def long(self, ticket, buy_date, share_price):
        if len(self.portfolios) <= 10:
            buy_amount = (self.balance * self.size) / share_price
            # self.init_cap -= buy_amount
            #new_portfolio = {"ticket": ticket, "buy_date": buy_date, "amount": buy_amount, "long": True, "sell_date": }
            # new_transaction = {"no": len(self.transactions), "ticket": ticket, "stra": "long", "date": buy_date, "amount": "-" + str(buy_amount), "remaining_capital": str(self.init_cap)}
            self.portfolios.append(new_portfolio)
            # self.transactions.append(new_transaction)
        else:
            pass

    def short(self):
        pass

    def empty(self, index):
        portfolio = self.portfolios.pop([index])
    
    def executeOrder(self, ticket, buy_data, share_price):
        pass

    def longShort(self, ticket, date, score):
        if score >= self.bmark_score:
            # long
            end_date = date + datetime.timedelta(days=7)
            buy_date, share_price = self.get_stock_data(ticket, date, end_date)
            self.long(ticket, buy_date, share_price)
        else:
            # short
            print(ticket + " score of " + str(score) + " is not greater than " + str(self.bmark_score))

    