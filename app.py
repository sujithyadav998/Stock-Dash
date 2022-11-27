import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from datetime import date 
from dash.dependencies import Input, Output, State
import yfinance as yf
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from model import prediction

app = dash.Dash(__name__)
server = app.server

# df = yf.download("PFI", "2018-01-22", "2019-01-22" )
# df.reset_index(inplace=True)

# def get_stock_price_fig(df):
#   fig = px.line(df,
#   x="Date", y="Open",
#   title="Closing and Opening Price vs Date")
#   return fig

item1 = html.Div(
[
html.H1("Welcome to the Stock Dash App!", className="start"),
html.Div([
# stock code input
 dcc.Input(value='', type='text',className="inputs",id = "inpt"),
 html.Button('Submit', id='submitbutton',className="btn",n_clicks=0)


]
),
html.Div([
# Date range picker input
dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(1995, 8, 5),
        max_date_allowed=dt.now(),
        initial_visible_month=dt.now(),
        end_date=dt.now().date()
    ), 
   
    
]),
html.Div([
# Stock price button
html.Button('stockprice', id='stockprice',className="btn"),

# Indicators button
html.Button('Indicators', id='Indicator',className="btn"),

# Number of days of forecast input
dcc.Input(value='', type='text',placeholder="number of days",className="inputs",id = "n_days"),

# Forecast button
html.Button('Forecast', id='forecast',className="btn")

],id = "inside"),
],
className="box1")

item2 = html.Div(
[
html.Div(
[ # Logo

html.Img(id = "lgc"),
# Company Name
html.Div(id = "header")
   #html.P("need to be chnaged")
],
),
html.Div( #Description
id="description", className="decription_ticker"),

html.Div([], id="graphs-content"),
html.Div([], id="main-content"),

html.Div([
# Forecast plot
], id="forecast-content")
],
className="content",)


app.layout = html.Div([item1, item2],className="container")



#dcc._css_dist[0][‘relative_package_path’].append(‘test.css’)
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True





#setting logo,companies name and description dynamically
@app.callback(
[
Output(component_id = "header", component_property = "children"),
Output("lgc","src"),
Output("description","children")
],
[Input("submitbutton","n_clicks")],
[State("inpt", "value")])

def update_data(n_clicks,inputdata):
    if(n_clicks == None ):
        return "Hey there! Please enter a legitimate stock code to get details.",None,None
    
    else:
        if(inputdata == None):
            raise PreventUpdate
        else:
            ticker = yf.Ticker(inputdata)
            inf = ticker.info
            df = pd.DataFrame().from_dict(inf, orient="index").T
            
            # for i in inf.keys():
            #   print(i,":",inf[i])
            return [inf["shortName"],inf["logo_url"] ,inf["longBusinessSummary"]]# input parameter(s)'



# callback for stocks graphs

def get_stock_price_fig(df):

    fig = px.line(df,
                  x="Date",
                  y=["Close", "Open"],
                  title="Closing and Openning Price vs Date")

    return fig

@app.callback([
    Output("graphs-content", "children"),
], [
    Input("stockprice", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("inpt", "value")])

def stock_price(n, start_date, end_date, val):
    if n == None:
        return [""]
        #raise PreventUpdate
    if val == None:
        raise PreventUpdate
    else:
        if start_date != None:
            df = yf.download(val, str(start_date), str(end_date))
        else:
            df = yf.download(val)

    df.reset_index(inplace=True)
    fig = get_stock_price_fig(df)
    return [dcc.Graph(figure=fig)]


# callback for indicators


def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                     x="Date",
                     y="EWA_20",
                     title="Exponential Moving Average vs Date")
    fig.update_traces(mode='lines+markers')
    return fig

@app.callback([Output("main-content", "children")], [
    Input("Indicator", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("inpt", "value")])

def indicators(n, start_date, end_date, val):
    if n == None:
        return [""]
    if val == None:
        return [""]

    if start_date == None:
        df_more = yf.download(val)
    else:
        df_more = yf.download(val, str(start_date), str(end_date))

    df_more.reset_index(inplace=True)
    fig = get_more(df_more)
    return [dcc.Graph(figure=fig)]

# callback for forecast
@app.callback([Output("forecast-content", "children")],
              [Input("forecast", "n_clicks")],
              [State("n_days", "value"),
               State("inpt", "value")])
def forecast(n, n_days, val):
    if n == None:
        return [""]
    if val == None:
        raise PreventUpdate
    fig = prediction(val, int(n_days) + 1)
    return [dcc.Graph(figure=fig)]


if __name__ == '__main__':
  app.run_server(debug=True)

#plotting price vs date graph 
# def get_stock_price_fig(df):
#   fig = px.line(df,
#   x="Date", y="Open",
#   title="Closing and Opening Price vs Date")
#   return fig


# @app.callback(
# [
# Output(component_id = "graphs-content", component_property = "figure")
# ],
# [
# Input("stockprice","n_clicks"),
# Input('my-date-picker-range', 'start_date'),
# Input('my-date-picker-range', 'end_date')
# ],
# [State("inpt", "value")])

# def update(n_clicks,startdate,enddate,inputdata):
#   df = yf.download(inputdata, startdate, enddate )
#   df.reset_index(inplace=True)
#   fig = get_stock_price_fig(df)
#   return [fig]
    

# # inputdata = "PFI"
# # ticker = yf.Ticker(inputdata)
# # inf = ticker.info
# # df = pd.DataFrame().from_dict(inf, orient="index").T
# # for i in inf.keys():
# #   print(i,":",inf[i])

# def get_more(df):
#   df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
#   fig = px.scatter(df,
#   x= "Date",
#   y= "EWA_20",
#   title="Exponential Moving Average vs Date")
#   fig.update_traces(mode= "lines")# appropriate mode)
#   return fig


# @app.callback(
# [
# Output(component_id = "main-content", component_property = "figure")
# ],
# [
# Input("Indicator","n_clicks"),
# Input('my-date-picker-range', 'start_date'),
# Input('my-date-picker-range', 'end_date')
# ],
# [State("inpt", "value")])

# def upd(n_clicks,startdate,enddate,inputdata):
#   df = yf.download(inputdata, startdate, enddate )
#   df.reset_index(inplace=True)
#   fig = get_more(df)
#   return [fig]
    

    

# # your function here

