import pandas as pd
from tenacity import retry, wait_fixed, stop_after_attempt, RetryError
import logging
import requests

logger = logging.getLogger(__name__)


class Orderbook():
    def __init__(self, ticker):
        self.ticker = ticker
        self.exchange_name = None
        self.exchange_api = None
        self.result_json = None
        self.perc_depth = None
        self.buy_orders = pd.DataFrame()
        self.sell_orders = pd.DataFrame()
        self.low_boundary_volume = None
        self.low_boundary = None
        self.high_boundary_volume = None
        self.high_boundary = None

    def get_depth_df(self):
        self.fetch_data()
        list_df =[]
        list_df.append(self.get_depth(2))
        list_df.append(self.get_depth(5))
        list_df.append(self.get_depth(10))
        list_df.append(self.get_depth(15))
        list_df.append(self.get_depth(20))
        list_df.append(self.get_depth(25))
        list_df.append(self.get_depth(30))
        return pd.DataFrame(list_df)


    def get_depth(self, perc_depth):
        self.perc_depth = perc_depth
        if self.result_json:
            self._set_sell_orders_df()
            self._set_buy_orders_df()
            self._calculate_high_boundary_volume()
            self._calculate_low_boundary_volume()

        return {
                "exchange": self.exchange_name,
                "perc_depth": self.perc_depth,
                "buy_vol": self.low_boundary_volume,
                "sell_vol": self.high_boundary_volume,
                "buy_level": self.low_boundary,
                "sell_level": self.high_boundary
                }

    def _set_exchange_api(self):
        pass

    @retry(wait=wait_fixed(10), stop=stop_after_attempt(5))
    def _request_json(self):
        result = requests.get(self.exchange_api).json()
        self.result_json= result
        return True

    def fetch_data(self):
        self._set_exchange_api()
        try:
            self._request_json()
        except RetryError:
            logger.error(f"Unable to get json data from the exchange {self.exchange_name}")       
    
    def _set_sell_orders_df(self):
        pass
    
    def _calculate_high_boundary_volume(self):
        sell = self.sell_orders.copy()
        sell = sell.assign(sell_volume=sell["Quantity"] * sell["Rate"])
        sell_limit = sell.Rate.min() * (1 + self.perc_depth/100)
        self.high_boundary = round(sell_limit,6)
        sell_vol = sell[sell.Rate < sell_limit]['sell_volume'].sum()
        self.high_boundary_volume = round(sell_vol,0)

    def _set_buy_orders_df(self):
        pass
    
    def _calculate_low_boundary_volume(self):
        buy = self.buy_orders.copy()
        buy = buy.assign(buy_volume=buy["Quantity"] * buy["Rate"])
        low_boundary = buy.Rate.max() * (1 - self.perc_depth/100)
        self.low_boundary = round(low_boundary,6)
        buy_volume = buy[buy.Rate > low_boundary]['buy_volume'].sum()
        self.low_boundary_volume = round(buy_volume,0)