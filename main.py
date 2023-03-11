import pandas as pd
from kaspabook.mexc_orderbook import MEXCOrderbook
from kaspabook.txbit_orderbook import TxbitOrderbook

from flask import Flask

app = Flask(__name__)


@app.route('/')
def get_orderbook():
    mexc_df = MEXCOrderbook("KAS/USDT").get_depth_df()
    txbit_df = TxbitOrderbook("KAS/USDT").get_depth_df()
    merged_orderbook = pd.concat([mexc_df,txbit_df])
    return merged_orderbook.to_html(header="true", table_id="table")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)