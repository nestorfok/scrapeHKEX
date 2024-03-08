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
        return stock_data.index[0].date(), stock_data.iloc[0]['Close']


    def strategy(self):
        start_date = datetime.datetime(2017, 4, 5).date()
        end_date = datetime.datetime(2017,8,31).date()
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
        
            self.cur_day += datetime.timedelta(days=1)
            #time.sleep(0.0005)

    def long(self, ticket, buy_date, buy_share_price, sell_date, sell_share_price):
        if len(self.portfolios) < 10:
            divisor = (self.size - len(self.portfolios))
            buy_amount = int((self.balance / divisor) / buy_share_price)

            # attach order
            buy_order = {"ticket": ticket, "date": buy_date, "amount": buy_amount * buy_share_price, "buy": True}
            sell_order = {"ticket": ticket, "date": sell_date, "amount": buy_amount * sell_share_price, "buy": False}
            self.buy_orders.append(buy_order)
            self.sell_orders.append(sell_order)

            # add to portfolio
            new_portfolio = {"ticket": ticket, "buy_date": buy_date, "sell_date": sell_date, "long": True}
            self.portfolios.append(new_portfolio)
            
            # self.init_cap -= buy_amount
            #new_portfolio = {"ticket": ticket, "buy_date": buy_date, "amount": buy_amount, "long": True, "sell_date": }
            # new_transaction = {"no": len(self.transactions), "ticket": ticket, "stra": "long", "date": buy_date, "amount": "-" + str(buy_amount), "remaining_capital": str(self.init_cap)}
            # self.portfolios.append(new_portfolio)
            # self.transactions.append(new_transaction)
        else:
            pass

    def daily_pl (self):
        try:
            pass
        except:
            pass

    def empty(self, index):
        portfolio = self.portfolios.pop([index])
    
    def executeOrder(self, order):
        if order["buy"] is True:
            self.balance -= order["amount"]
            new_transaction = {"ticket": order["ticket"], "date": order["date"], "amount": "-" + str(order["amount"]), "remaining_capital": str(self.balance)}
        else:
            self.balance += order["amount"]
            new_transaction =  {"ticket": order["ticket"], "date": order["date"], "amount": "+" + str(order["amount"]), "remaining_capital": str(self.balance)}
        self.transactions.append(new_transaction)

    def longShort(self, ticket, date, score):
        if score >= self.bmark_score:
            # long
            # get buy_date, sell_date, buy_share_price, sell_share_price
            print(ticket + " score of " + str(score) + " is greater than " + str(self.bmark_score))
            end_date = date + datetime.timedelta(days=7)
            #print(date, end_date)
            buy_date, buy_share_price = self.get_stock_data(ticket, date, end_date)
            print(buy_date, buy_share_price)
            sell_date, sell_share_price = self.get_stock_data(ticket, buy_date + datetime.timedelta(days=7), buy_date + datetime.timedelta(days=14))
            
            self.long(ticket, buy_date, buy_share_price, sell_date, sell_share_price)
        else:
            # short
            print(ticket + " score of " + str(score) + " is not greater than " + str(self.bmark_score))

if __name__ == "__main__":
    ESG_score_2017  = pd.read_csv("../ESG_score/ESG_data_2017.csv")
    ESG_score_2018  = pd.read_csv("../ESG_score/ESG_data_2018.csv")
    ESG_score_2019  = pd.read_csv("../ESG_score/ESG_data_2019.csv")
    ESG_score_2020  = pd.read_csv("../ESG_score/ESG_data_2020.csv")
    ESG_score_2021  = pd.read_csv("../ESG_score/ESG_data_2021.csv")
    ESG_score_2022  = pd.read_csv("../ESG_score/ESG_data_2022.csv")

    ESG_report = pd.read_csv("../ESG_report/concatenatedESGData.csv")
    ESG_report = ESG_report.drop(['Unnamed: 0'], axis=1)

    ESG_report['ESG_2017_rel_date'] = pd.to_datetime(ESG_report['ESG_2017_rel_date'], format='%d/%m/%Y')
    ESG_report['ESG_2018_rel_date'] = pd.to_datetime(ESG_report['ESG_2018_rel_date'], format='%d/%m/%Y')
    ESG_report['ESG_2019_rel_date'] = pd.to_datetime(ESG_report['ESG_2019_rel_date'], format='%d/%m/%Y')
    ESG_report['ESG_2020_rel_date'] = pd.to_datetime(ESG_report['ESG_2020_rel_date'], format='%d/%m/%Y')
    ESG_report['ESG_2021_rel_date'] = pd.to_datetime(ESG_report['ESG_2021_rel_date'], format='%d/%m/%Y')
    ESG_report['ESG_2022_rel_date'] = pd.to_datetime(ESG_report['ESG_2022_rel_date'], format='%d/%m/%Y')
    ESG_report['ESG_2023_rel_date'] = pd.to_datetime(ESG_report['ESG_2023_rel_date'], format='%d/%m/%Y')
    ESG_report = ESG_report.drop(563)

    portfolio = Portfolio(1000000, 10, 10, ESG_report, ESG_score_2017, ESG_score_2018, ESG_score_2019, ESG_score_2020, ESG_score_2021, ESG_score_2022)
    
    print(portfolio.get_balance())

    print("______________start______________")

    portfolio.strategy()
    # portfolio.set_balance(100)

    print("_____________end______________")

    print(portfolio.get_balance())

    transactions = portfolio.get_transactions()
    for i in transactions:
        print(i)
        print("________________________________")
