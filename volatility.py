from math import sqrt
from operator import index
import pandas as pd
import numpy as np

class Volatility:
    def __init__(self, type: str = "C-to-C", frequency: str = "daily", period: int = 21):
        # self.sessions_in_year = sessions_in_year
        self.type = type
        self.frequency = frequency
        self.period = period

        types = ["C-to-C", "Parkinson", "G-K"]
        frequencies = ["intraday", "daily", "weekly", "monthly"]
        assert type in types, f"{type} is not in the list of supported volatility type {types}"
        assert frequency in frequencies, f"{frequency} is not in the list of supported frequencies {frequencies}"

    def get_return_frequency(self) -> int:
        if self.frequency == "daily": return 252
        if self.frequency == "weekly": return 52
        if self.frequency == "monthly": return 12
        return 252 # default value
    
    def cal_log_return(self, market_px: pd.DataFrame, from_px: str = "Close", to_px: str = "Close", shift: int = -1) -> pd.DataFrame:
        ret = np.log(market_px[to_px] / market_px[from_px].shift(shift)) # log return
        ret_dat = pd.DataFrame({"Return": ret}).set_index(market_px.index).dropna(axis=0)
        return ret_dat
    
    def cal_ann_volatility(self, market_px: pd.DataFrame, zero_drift: bool = False) -> pd.DataFrame:
        F = self.get_return_frequency()
        N = self.period # John Hull definition: n-day volatility uses N returns
        n_pxs = market_px.shape[0]
        ann_vols = []
        ann_vol_dat = pd.DataFrame()

        if self.type == "C-to-C":
            for i in range(0, n_pxs - self.period):
                sample_ret = self.cal_log_return(market_px.iloc[i:(i+self.period+1)], from_px="Close", to_px="Close", shift=-1) 
                if zero_drift: # assuming zero deviation from avg. log return
                    ssq_ret = np.sum(np.square(sample_ret["Return"])) # sum-of-squared_return = sum(r_i^2)
                    ann_vols.append(np.sqrt(F/(N-1)) * np.sqrt(ssq_ret)) # ann_vol = sqrt(F/(N-1)) * sqrt(sum-of-squared_return)
                else:
                    std_dev = np.sqrt(F) * np.std(sample_ret["Return"]) # standard_deviation = sqrt(F/N) * sqrt(sum((r_i - r_bar)^2))
                    ann_vols.append(np.sqrt(N/(N-1)) * std_dev) # ann_vol = sqrt(N/(N-1)) * standard_deviation
            ann_vol_dat = pd.DataFrame({'Ann_Volatility': ann_vols}).set_index(market_px.index[:-self.period])
        elif self.type == "Parkinson":
            for i in range(0, n_pxs - self.period + 1):
                sample_ret = self.cal_log_return(market_px.iloc[i:(i+self.period+1)], from_px="Low", to_px="High", shift=0)
                ssq_ret = np.sum(np.square(sample_ret["Return"])) # sum-of-squared_return = sum(r_i^2)
                ann_vols.append(np.sqrt(F/N) * np.sqrt(1/(4*np.log(2)) * ssq_ret)) # ann_vol = sqrt(F/N) * sqrt(1/(4*ln(2)) * sum-of-squared_return)
            ann_vol_dat = pd.DataFrame({'Ann_Volatility': ann_vols}).set_index(market_px.index[:-self.period + 1])
        elif self.type == "G-K":
            for i in range(0, n_pxs - self.period + 1):
                sample_ret_lh = self.cal_log_return(market_px.iloc[i:(i+self.period+1)], from_px="Low", to_px="High", shift=0)
                sample_ret_oc = self.cal_log_return(market_px.iloc[i:(i+self.period+1)], from_px="Open", to_px="Close", shift=0)
                ssq_ret_lh = np.sum(np.square(sample_ret_lh["Return"]))
                ssq_ret_oc = np.sum(np.square(sample_ret_oc["Return"]))
                ann_vols.append(np.sqrt(F/N) * np.sqrt(0.5*ssq_ret_lh - (2*np.log(2) - 1)*ssq_ret_oc))
            ann_vol_dat = pd.DataFrame({'Ann_Volatility': ann_vols}).set_index(market_px.index[:-self.period + 1])
            
        return ann_vol_dat


