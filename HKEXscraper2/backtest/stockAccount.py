import datetime
from broker import Broker

class StockAccount():

    def __init__(self, init_cap):
        self.init_cap = init_cap
        self.cash = init_cap
        self.lock_cap = 0
        self.portfolios = []
        self.buy_orders = []
        self.sell_orders = []
        self.transactions = []
        self.daily_pls = []
        self.broker = Broker()
    
    # Getters
    def get_cash(self):
        return self.cash
    
    def get_lock_cap(self):
        return self.lock_cap
    
    def get_portfolios(self):
        return self.portfolios
    
    def get_buy_orders(self):
        return self.buy_orders
    
    def get_sell_orders(self):
        return self.sell_orders
    
    def get_daily_pls(self):
        return self.daily_pls
    
    def get_transactions(self):
        return self.transactions
    
    def set_porfolios(self, porfolios: list):
        self.portfolios = porfolios
    
    def set_buy_orders(self, buy_orders: list):
        self.buy_orders = buy_orders

    def set_sell_orders(self, sell_orders: list):
        self.sell_orders = sell_orders
    
    def send_buy_order(self, ticker, long, buy, date, amount):
        buy_order = {"ticker": ticker, "long": long, "buy": buy, "date": date, "amount": amount}
        self.lock_cap += buy_order["amount"]
        self.buy_orders.append(buy_order)
    
    def send_sell_order(self, ticker, long, buy, date, amount):
        sell_order = {"ticker": ticker, "long": long, "buy": buy, "date": date, "amount": amount}
        self.sell_orders.append(sell_order)
    
    def new_portfolio(self, ticker, long, buy_date, sell_date, num_shares, share_price):
        portfolio = {"ticker": ticker, "long": long, "buy_date": buy_date, "sell_date": sell_date, "num_shares": num_shares, "share_price": share_price}
        self.portfolios.append(portfolio)
    
    def execute_order(self, order):
        if order["long"] is True:
            if order["buy"] is True:
                self.cash -= order["amount"]
                self.lock_cap -= order["amount"]
                new_transaction = {"ticker": order["ticker"], "date": order["date"], "amount": "-" + str(order["amount"]), "remaining_capital": str(self.cash)}
            else:
                self.cash += order["amount"]
                new_transaction =  {"ticker": order["ticker"], "date": order["date"], "amount": "+" + str(order["amount"]), "remaining_capital": str(self.cash)}
            
            self.transactions.append(new_transaction)

    def cal_daily_pl(self, cur_day):
        cash_balance = self.cash + self.lock_cap
        stock_balance = 0

        for portfolio in self.portfolios:
            if portfolio["long"] is True:
                date, share_price = self.broker.get_stock_price(portfolio["ticker"], cur_day, cur_day + datetime.timedelta(days=1))
                stock_balance += share_price * portfolio["num_shares"]
            
        daily_pl = {"date": cur_day, "pl": (cash_balance + stock_balance) - self.init_cap, "balance": cash_balance + stock_balance}
        self.daily_pls.append(daily_pl)

