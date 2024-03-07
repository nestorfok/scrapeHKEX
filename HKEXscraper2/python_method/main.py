# This is a sample Python script.
import pandas as pd
import yfinance as yf
import re
# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def grouping(n: int, df):
    lst = []
    group = n// 5
    end_idx = 0
    for i in range(4):
        lst.append(group + end_idx)
        end_idx += group
    lst.append(n)
    return df[:lst[0]], df[lst[0]:lst[1]], df[lst[1]:lst[2]], df[lst[2]:lst[3]], df[lst[3]:lst[4]]

def getPortfolioDetail(portfolio, stock_df_year, ESG_data_year_group):
    for i in ESG_data_year_group.index:
        row = stock_df_year.loc[stock_df_year['Ticker'] == ESG_data_year_group.loc[i]['file_name']]
        portfolio = pd.concat([portfolio, row], ignore_index=True)
    return portfolio

def obainPorfolioGain(stock_df_year, ESG_data_year_g1, ESG_data_year_g2, ESG_data_year_g3, ESG_data_year_g4, ESG_data_year_g5):
    stock_df_columns = stock_df_year.columns.tolist()
    port_1_empty = pd.DataFrame(columns=stock_df_columns)
    port_2_empty = pd.DataFrame(columns=stock_df_columns)
    port_3_empty = pd.DataFrame(columns=stock_df_columns)
    port_4_empty = pd.DataFrame(columns=stock_df_columns)
    port_5_empty = pd.DataFrame(columns=stock_df_columns)
    port_1 = getPortfolioDetail(port_1_empty, stock_df_year, ESG_data_year_g1)
    port_2 = getPortfolioDetail(port_2_empty, stock_df_year, ESG_data_year_g2)
    port_3 = getPortfolioDetail(port_3_empty, stock_df_year, ESG_data_year_g3)
    port_4 = getPortfolioDetail(port_4_empty, stock_df_year, ESG_data_year_g4)
    port_5 = getPortfolioDetail(port_5_empty, stock_df_year, ESG_data_year_g5)
    return port_1, port_2, port_3, port_4, port_5

def getMean(stock_return_year_g1, stock_return_year_g2, stock_return_year_g3, stock_return_year_g4, stock_return_year_g5):
    mean_profit_g1 = stock_return_year_g1["Yearly Profit"].mean()
    mean_profit_g2 = stock_return_year_g2["Yearly Profit"].mean()
    mean_profit_g3 = stock_return_year_g3["Yearly Profit"].mean()
    mean_profit_g4 = stock_return_year_g4["Yearly Profit"].mean()
    mean_profit_g5 = stock_return_year_g5["Yearly Profit"].mean()
    return mean_profit_g1, mean_profit_g2,mean_profit_g3,mean_profit_g4,mean_profit_g5

def getYealyData(df, year):
    new_df = pd.DataFrame()
    for row in df.index:
        file_name = df.loc[row]['file_name']
        if re.search(f"^{year}", file_name):
            new_df = new_df.append(df.loc[row], ignore_index = True)
    return new_df

def get_stock_data(ticker: str, start_date_1, start_date_2, end_date_1, end_date_2):
    #print(ticker)
    #print(start_date_1)
    stock_start = yf.download(ticker, start=start_date_1, end=start_date_2, group_by='tickers')
    stock_end = yf.download(ticker, start=end_date_1, end=end_date_2, group_by='tickers')
    return stock_start, stock_end

def convertToStockCode(df):
    for i in df.index:
        name = df.loc[i]['file_name'][6:10] + ".HK"
        #print(name)
        df.loc[i, 'file_name'] = name
    return df

def tickerToAString(df):
    resultChunk = ""
    for row in df.index:
        resultChunk = resultChunk + " " + df.loc[row]['file_name']
    return resultChunk[1:]


def aggregateStockDate(ticker_year, stock_start, stock_end, start_date, end_date):
    stock_columns = [
        'Ticker',
        f'Price on {start_date}',
        f'Price on {end_date}',
        'Yearly Profit'
    ]
    stock_df = pd.DataFrame(columns=stock_columns)

    ticker_year_list = ticker_year.split()
    for ticker in ticker_year_list:
        start_price = stock_start.loc[start_date][ticker]['Close']
        end_price = stock_end.loc[end_date][ticker]['Close']
        row = pd.DataFrame(
            [[
                ticker,
                start_price,
                end_price,
                (end_price - start_price) / start_price * 100
            ]], columns=stock_columns
        )
        stock_df = pd.concat([stock_df, row], ignore_index=True)
    return stock_df