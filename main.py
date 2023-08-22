import pandas as pd
from kaspabook.mexc_orderbook import MEXCOrderbook
from kaspabook.txbit_orderbook import TxbitOrderbook
from kaspabook.graph import create_depth_fig
import plotly
import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def depth_chart():
    mexc_df = MEXCOrderbook("KAS/USDT").calculate_cumsum_df()
    fig_mexc = create_depth_fig(mexc_df, "MEXC")
    graphJSON_mexc = json.dumps(fig_mexc, cls=plotly.utils.PlotlyJSONEncoder)

    # txbit_df = TxbitOrderbook("RXD/USDT").calculate_cumsum_df()
    # fig_txbit = create_depth_fig(txbit_df, "TXBIT")
    # graphJSON_mtxbit = json.dumps(fig_txbit, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('orderbooks.html', graphJSON_mexc=graphJSON_mexc, graphJSON_txbit= graphJSON_mexc )

@app.route('/data')
def get_orderbook():
    mexc_df = MEXCOrderbook("KAS/USDT").get_depth_df()
    #txbit_df = TxbitOrderbook("KAS/USDT").get_depth_df()
    merged_orderbook = pd.concat([mexc_df])
    return merged_orderbook.to_html(header="true", table_id="table")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)