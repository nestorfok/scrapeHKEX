import pandas as pd
import numpy as np
import datetime
import time
import yfinance as yf
from portfolio import Portfolio

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

    portfolio = Portfolio(init_cap=1000000, size=10, bmark_score=30, report=ESG_report, score_2017=ESG_score_2017, 
                          score_2018=ESG_score_2018, score_2019=ESG_score_2019, score_2020=ESG_score_2020, 
                          score_2021=ESG_score_2021, score_2022=ESG_score_2022)
    
    print(portfolio.get_balance())

    print("______________start______________")

    portfolio.strategy(start_date='01-01-2018', end_date='31-12-2018')
    # portfolio.set_balance(100)

    print("_____________end________________")

    print(portfolio.get_balance())

    print("_________transactions___________")

    transactions = portfolio.get_transactions()
    for i in transactions:
        print(i)
    
    print("_______end transactions________")

    daily_pls = portfolio.get_daily_pls()
    for daily_pl in daily_pls:
        print("date: " + daily_pl["date"].strftime("%d-%m-%Y") + ", pl: " + str(daily_pl["pl"]) + ", balance: " + str(daily_pl["balance"]))
