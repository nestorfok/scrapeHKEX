import pandas as pd
import numpy as np
import yfinance as yf
from strategy import Strategy
from broker import Broker
import datetime

if __name__ == "__main__":
    # ESG_score_2017  = pd.read_csv("../ESG_score/ESG_data_2017.csv")
    # ESG_score_2018  = pd.read_csv("../ESG_score/ESG_data_2018.csv")
    # ESG_score_2019  = pd.read_csv("../ESG_score/ESG_data_2019.csv")
    # ESG_score_2020  = pd.read_csv("../ESG_score/ESG_data_2020.csv")
    # ESG_score_2021  = pd.read_csv("../ESG_score/ESG_data_2021.csv")
    # ESG_score_2022  = pd.read_csv("../ESG_score/ESG_data_2022.csv")

    # ESG_report = pd.read_csv("../ESG_report/concatenatedESGData.csv")
    # ESG_report = ESG_report.drop(['Unnamed: 0'], axis=1)

    # ESG_report['ESG_2017_rel_date'] = pd.to_datetime(ESG_report['ESG_2017_rel_date'], format='%d/%m/%Y')
    # ESG_report['ESG_2018_rel_date'] = pd.to_datetime(ESG_report['ESG_2018_rel_date'], format='%d/%m/%Y')
    # ESG_report['ESG_2019_rel_date'] = pd.to_datetime(ESG_report['ESG_2019_rel_date'], format='%d/%m/%Y')
    # ESG_report['ESG_2020_rel_date'] = pd.to_datetime(ESG_report['ESG_2020_rel_date'], format='%d/%m/%Y')
    # ESG_report['ESG_2021_rel_date'] = pd.to_datetime(ESG_report['ESG_2021_rel_date'], format='%d/%m/%Y')
    # ESG_report['ESG_2022_rel_date'] = pd.to_datetime(ESG_report['ESG_2022_rel_date'], format='%d/%m/%Y')
    # ESG_report['ESG_2023_rel_date'] = pd.to_datetime(ESG_report['ESG_2023_rel_date'], format='%d/%m/%Y')
    # ESG_report = ESG_report.drop(563)

    strategy = Strategy(init_cap=1000000, size=10, bmark='positive', bmark_score=30)
    
    print(strategy.stock_account.get_cash())

    print("______________start______________")

    strategy.ESGstrategy1(start_date='01-01-2018', end_date='31-12-2018')
    # portfolio.set_balance(100)

    print("_____________end________________")

    # for i in strategy.stock_account.get_daily_pls():
    #     print(i)

    print("_____________end________________")

    # for j in strategy.stock_account.get_transaction():
    #     print(j)
    #print(strategy.stock_account.get_transaction())

    # print("_________transactions___________")

    # transactions = portfolio.get_transactions()
    # for i in transactions:
    #     print(i)
    
    # print("_______end transactions________")

    # daily_pls = portfolio.get_daily_pls()
    # for daily_pl in daily_pls:
    #     print("date: " + daily_pl["date"].strftime("%d-%m-%Y") + ", pl: " + str(daily_pl["pl"]) + ", balance: " + str(daily_pl["balance"]))
    # broker = Broker(file_name="trading_holidays.txt")
    # start_date = datetime.datetime.strptime('02-01-2018', '%d-%m-%Y').date()
    # print(broker.is_trading_day(cur_day=start_date))