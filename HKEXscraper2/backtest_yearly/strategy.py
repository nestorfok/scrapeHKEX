import datetime
import math
from broker import Broker
from stockAccount import StockAccount
import pandas as pd
import time

class Strategy:
    
    def __init__(self, init_cap, size, bmark, bmark_score):
        self.size = size # 10

        self.bmark = bmark

        self.bmark_score = bmark_score # 30

        self.__import_data()

        self.cur_day = None

        self.broker = Broker(file_name="trading_holidays.txt")
        self.stock_account = StockAccount(init_cap=init_cap)


    def __import_data(self):
        self.score_2017  = pd.read_csv("../ESG_score/ESG_data_2017.csv")
        self.score_2018  = pd.read_csv("../ESG_score/ESG_data_2018.csv")
        self.score_2019  = pd.read_csv("../ESG_score/ESG_data_2019.csv")
        self.score_2020  = pd.read_csv("../ESG_score/ESG_data_2020.csv")
        self.score_2021  = pd.read_csv("../ESG_score/ESG_data_2021.csv")
        self.score_2022  = pd.read_csv("../ESG_score/ESG_data_2022.csv")

        self.report = pd.read_csv("../ESG_report/concatenatedESGData.csv")
        # self.report = self.report.drop(['Unnamed: 0'], axis=1)
        self.__modify_report()

    def __modify_report(self):
        self.report = self.report.drop(['Unnamed: 0'], axis=1)

        self.report['ESG_2017_rel_date'] = pd.to_datetime(self.report['ESG_2017_rel_date'], format='%d/%m/%Y')
        self.report['ESG_2018_rel_date'] = pd.to_datetime(self.report['ESG_2018_rel_date'], format='%d/%m/%Y')
        self.report['ESG_2019_rel_date'] = pd.to_datetime(self.report['ESG_2019_rel_date'], format='%d/%m/%Y')
        self.report['ESG_2020_rel_date'] = pd.to_datetime(self.report['ESG_2020_rel_date'], format='%d/%m/%Y')
        self.report['ESG_2021_rel_date'] = pd.to_datetime(self.report['ESG_2021_rel_date'], format='%d/%m/%Y')
        self.report['ESG_2022_rel_date'] = pd.to_datetime(self.report['ESG_2022_rel_date'], format='%d/%m/%Y')
        self.report['ESG_2023_rel_date'] = pd.to_datetime(self.report['ESG_2023_rel_date'], format='%d/%m/%Y')

        #self.report = self.report.drop(563)

    def ESGstrategy1(self, start_date, end_date):
        start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').date()
        end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y').date()
        self.cur_day = start_date
        report_cols = self.report.columns.values.tolist()[1:]
        #print(report_cols)

        while self.cur_day != end_date:

            if self.broker.is_trading_day(self.cur_day) is False:
                #print(self.cur_day.strftime("%d-%m-%Y") + " is not trading!")
                self.cur_day += datetime.timedelta(days=1)
                # time.sleep(1)
                continue
            
            # loop through each stock
            for index, row in self.report.iterrows():
                #print("asdsadjafds,fdksfhkdsahfksdf")
                stock_code = row['stock_code'][1:]
                # loop through each yearly ESG_report
                for col in reversed(report_cols):
                    #print(col)
                    #time.sleep(1)
                    if row[col].date() == self.cur_day:
                        year = self.cur_day.year
                        #print(year)
                        #time.sleep(100)
                        if year == 2017:
                            #print("yes")
                            score = self.score_2017.loc[self.score_2017['file_name'] == stock_code][self.bmark]
                            score = score.values[0]
                            if score >= self.bmark_score and len(self.stock_account.get_portfolios()) < self.size:
                                self.long(ticker=stock_code, date=self.cur_day)
                            break
                        elif year == 2018:
                            #print("yes")
                            score = self.score_2018.loc[self.score_2018['file_name'] == stock_code][self.bmark]
                            if len(score) != 0 and score.values[0] >= self.bmark_score and len(self.stock_account.get_portfolios()) < self.size:
                                self.long(ticker=stock_code, date=self.cur_day)
                            break
                        elif year == 2019:
                            score = self.score_2019.loc[self.score_2019['file_name'] == stock_code][self.bmark]
                            if len(score) != 0 and score.values[0] >= self.bmark_score and len(self.stock_account.get_portfolios()) < self.size:
                                self.long(ticker=stock_code, date=self.cur_day)
                            break
                        elif year == 2020:
                            score = self.score_2020.loc[self.score_2020['file_name'] == stock_code][self.bmark]
                            if len(score) != 0 and score.values[0] >= self.bmark_score and len(self.stock_account.get_portfolios()) < self.size:
                                self.long(ticker=stock_code, date=self.cur_day)
                            break
                        elif year == 2021:
                            score = self.score_2021.loc[self.score_2021['file_name'] == stock_code][self.bmark]
                            if len(score) != 0 and score.values[0] >= self.bmark_score and len(self.stock_account.get_portfolios()) < self.size:
                                self.long(ticker=stock_code, date=self.cur_day)
                            break
                        elif year == 2022:
                            score = self.score_2022.loc[self.score_2022['file_name'] == stock_code][self.bmark]
                            if len(score) != 0 and score.values[0] >= self.bmark_score and len(self.stock_account.get_portfolios()) < self.size:
                                self.long(ticker=stock_code, date=self.cur_day)
                            break
                          
            #print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            #time.sleep(1)
            cur_portfolios = []
            cur_buy_orders = []
            cur_sell_orders = []

            for portfolio in self.stock_account.get_portfolios():
                if portfolio["long"] is True:
                    if portfolio["sell_date"] != self.cur_day:
                        cur_portfolios.append(portfolio)
            
            for buy_order in self.stock_account.get_buy_orders():
                if buy_order["date"] == self.cur_day:
                    self.stock_account.execute_order(order=buy_order)
                else:
                    cur_buy_orders.append(buy_order)

            for sell_order in self.stock_account.get_sell_orders():
                if sell_order["date"] == self.cur_day:
                    # print("hiiiiiii")
                    # time.sleep(100)
                    self.stock_account.execute_order(order=sell_order)
                else:
                    cur_sell_orders.append(sell_order)
            
            self.stock_account.set_porfolios(porfolios=cur_portfolios)
            self.stock_account.set_buy_orders(buy_orders=cur_buy_orders)
            self.stock_account.set_sell_orders(sell_orders=cur_sell_orders)
            # print(self.stock_account.get_sell_orders())
            # time.sleep(0.05)
            self.stock_account.cal_daily_pl(self.cur_day)

            self.cur_day += datetime.timedelta(days=1)

    def long(self, ticker, date):
        print("Buying " + ticker)

        buy_date, buy_share_price = self.broker.get_stock_price(ticker, date, date + datetime.timedelta(days=1))
        # print(buy_share_price, buy_date)
        sell_date, sell_share_price = self.broker.get_stock_price(ticker, buy_date + datetime.timedelta(days=31), buy_date + datetime.timedelta(days=38))
        # print(sell_date, sell_share_price)

        net_cap = self.stock_account.get_cash() - self.stock_account.get_lock_cap()
        portfolios_size = len(self.stock_account.get_portfolios())
        num_shares = math.floor((net_cap / (self.size - portfolios_size)) / buy_share_price)

        self.stock_account.send_buy_order(ticker=ticker, long=True, buy=True, date=buy_date, amount=num_shares * buy_share_price)
        self.stock_account.send_sell_order(ticker=ticker, long=True, buy=False, date=sell_date, amount=num_shares * sell_share_price)

        # print(self.stock_account.get_sell_orders())
        # print("***********************")

        self.stock_account.new_portfolio(ticker=ticker, long=True, buy_date=buy_date, sell_date=sell_date, num_shares=num_shares, share_price=buy_share_price)

