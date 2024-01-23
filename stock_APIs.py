from ast import List
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
import yfinance as yf
from datetime import datetime

class StockAPI:
    def __init__ (self, key: str, rapidapi: bool = False):
        self.key = key
        self.rapidapi = rapidapi

    def init_timeseries(self, output_format: str, indexing_type: str):
        ts = TimeSeries(key=self.key, output_format=output_format, indexing_type=indexing_type)
        return ts
    
    def get_market_px(
            self, symbol: str, frequency: str = "intraday", interval: str = "15min", 
            outputsize: str = "compact", output_format: str = "pandas", indexing_type: str = "date",
    ):
        frequencies = ["intraday", "daily", "daily_adjusted", "weekly", "weekly_adjusted", "monthly", "monthly_adjusted"]
        intervals = ["1min", "5min", "15min", "30min", "60min"]
        assert frequency in frequencies, f"{frequency} is not in the list of supported frequencies {frequencies}"
        if frequency == "intraday":
            assert interval in intervals, f"{interval} is not in the list of supported interval {interval} for intraday frequency"
        
        ts = self.init_timeseries(output_format=output_format, indexing_type=indexing_type)
        data = pd.DataFrame()
        meta_data = dict()

        if frequency == "intraday":
            data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
        elif frequency == "daily":
            data, meta_data = ts.get_daily(symbol=symbol, outputsize=outputsize)
        elif frequency == "daily_adjusted":
            data, meta_data = ts.get_daily_adjusted(symbol=symbol, outputsize=outputsize)
        elif frequency == "weekly":
            data, meta_data = ts.get_weekly(symbol=symbol)
        elif frequency == "weekly_adjusted":
            data, meta_data = ts.get_weekly_adjusted(ts)
        elif frequency == "weekly":
            data, meta_data = ts.get_monthly(symbol=symbol)
        elif frequency == "weekly_adjusted":
            data, meta_data = ts.get_monthly_adjusted(symbol=symbol)
        
        data = pd.DataFrame(data)
        data.columns = ["Open", "High", "Low", "Close", "Volume"]
        return data, meta_data
        
        
    
    # def get_intraday_px(self, ts: TimeSeries):
    #     data, meta_data = ts.get_intraday(symbol=self.symbol, interval=self.interval, outputsize=self.outputsize)
    #     return data, meta_data
    
    # def get_daily_px(self, ts: TimeSeries):
    #     data, meta_data = ts.get_daily(symbol=self.symbol, outputsize=self.outputsize)
    #     return data, meta_data
    
    # def get_daily_adjusted_px(self, ts: TimeSeries):
    #     data, meta_data = ts.get_daily_adjusted(symbol=self.symbol, outputsize=self.outputsize)
    #     return data, meta_data

    # def get_weekly_px(self,  ts: TimeSeries):
    #     data, meta_data = ts.get_weekly(symbol=self.symbol)
    #     return data, meta_data

    # def get_weekly_adjusted_px(self, ts: TimeSeries):
    #     data, meta_data = ts.get_weekly_adjusted(symbol=self.symbol)
    #     return data, meta_data

    # def get_monthly_px(self,  ts: TimeSeries):
    #     data, meta_data = ts.get_monthly(symbol=self.symbol)
    #     return data, meta_data

    # def get_monthly_adjusted_px(self,  ts: TimeSeries):
    #     data, meta_data = ts.get_monthly_adjusted(symbol=self.symbol)
    #     return data, meta_data
    