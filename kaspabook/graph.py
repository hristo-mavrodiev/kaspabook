import plotly
import plotly.express as px
import plotly.graph_objects as go

def create_depth_fig(df, title):
    fig= go.Figure()
    buy_df = df[df["side"] =="buy"]
    sell_df = df[df["side"] =="sell"]
    fig.add_trace(go.Scatter(x=buy_df["Rate"], y=buy_df["sum_USD"], fill='tozeroy',
                        name='buys'
                        #mode='none' # override default markers+lines
                        ))
    fig.add_trace(go.Scatter(x=sell_df["Rate"], y=sell_df["sum_USD"], fill='tozeroy',
                        name="sells"
                        #mode='none' # override default markers+lines
                        ))
    fig.update_layout(title=title)
    return fig
