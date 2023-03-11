import pandas as pd
import requests
from kaspabook.orderbook import Orderbook 
import logging

class MEXCOrderbook(Orderbook):
    def __init__(self, ticker):
        super().__init__(ticker)
        self.exchange_name = "MEXC"

    def _set_exchange_api(self):
        mexc_ticker = self.ticker.replace('/','')
        self.exchange_api = f"https://api.mexc.com/api/v3/depth?symbol={mexc_ticker}&limit=5000"

    def _set_sell_orders_df(self):
        asks = pd.DataFrame(self.result_json['asks'], columns=["Rate", "Quantity"])
        asks["Rate"] = asks["Rate"].astype(float)
        asks["Quantity"] = asks["Quantity"].astype(float)
        self.sell_orders = asks.copy()

    def _set_buy_orders_df(self):
        bids = pd.DataFrame(self.result_json['bids'], columns=["Rate", "Quantity"])
        bids["Rate"] = bids["Rate"].astype(float)
        bids["Quantity"] = bids["Quantity"].astype(float)
        self.buy_orders = bids.copy()
    


if __name__ == "__main__":
    mexc = MEXCOrderbook("KAS/USDT")
    print(mexc.get_depth_df())
