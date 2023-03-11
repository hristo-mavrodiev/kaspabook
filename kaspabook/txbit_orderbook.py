import pandas as pd
import requests
from kaspabook.orderbook import Orderbook
import logging

logger = logging.getLogger(__name__)

class TxbitOrderbook(Orderbook):
    def __init__(self, ticker):
        super().__init__(ticker)
        self.exchange_name = "TXBIT"

    def _set_exchange_api(self):
        txbit_ticker = self.ticker
        self.exchange_api = f"https://api.txbit.io/api/public/getorderbook?market={txbit_ticker}&type=both"
    
    def _set_buy_orders_df(self):
        buy = pd.DataFrame(self.result_json['result']['buy'])
        self.buy_orders = buy.copy()

    def _set_sell_orders_df(self):
        sell = pd.DataFrame(self.result_json['result']['sell'])
        self.sell_orders = sell.copy()
    


if __name__ == "__main__":
    txbit = TxbitOrderbook("KAS/USDT")
    print(txbit.get_depth_df())