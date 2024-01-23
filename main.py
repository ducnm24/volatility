import pandas as pd
import numpy as np
from datetime import datetime as dt
from alpha_vantage.timeseries import TimeSeries

from stock_APIs import StockAPI
from volatility import Volatility

key = '4DO6XBL174UG5TCE'
symbol = r'GOOGL'
sessions_in_year = 252

stock_api = StockAPI(key=key)
daily_mkt_px, meta_data = stock_api.get_market_px(symbol=symbol, frequency="daily")
daily_mkt_px.index = pd.to_datetime(daily_mkt_px.index).strftime('%Y-%m-%d')

vol = Volatility(type="C-to-C", frequency="daily", period=21)
daily_ret = vol.cal_log_return(daily_mkt_px, from_px="Low", to_px="High", shift=0)

ann_vol = vol.cal_ann_volatility(market_px=daily_mkt_px, zero_drift=True)

with pd.ExcelWriter("output.xlsx", engine='openpyxl') as f:
    daily_mkt_px.to_excel(f, sheet_name="daily_px")
    daily_ret.to_excel(f, sheet_name="daily_ret")
    ann_vol.to_excel(f, sheet_name="ann_vol")