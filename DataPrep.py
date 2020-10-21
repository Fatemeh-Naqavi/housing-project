from statistics import NormalDist
import scipy.stats as stats
import numpy as np
import pandas as pd
from bisect import bisect_right 


def one_month_data(data_frame):
    return data_frame.loc[data_frame['contract_date_as_days'] < 671].copy() #671 for all first month

# %%

def get_available_ads_index(index_row, base_contract_date, ad_info):
    available_ads = []
    for j, item in enumerate(ad_info['contract_date_as_days']):
        idx = ad_info.index[j]        
        ad_date = ad_info['ad_published_date_as_days'].loc[idx]
        if ad_date > base_contract_date:
            break
        other_contract_date = ad_info['contract_date_as_days'].loc[idx]
        day_between_contract_dates = base_contract_date - other_contract_date
        if day_between_contract_dates < 1:
            available_ads.append(ad_info.index[j])
    return available_ads

def get_availabe_ads_new_method(contract_info_one_month, ad_info_one_month):
    av_df = pd.DataFrame(index = contract_info_one_month.index, columns = ['av']).astype(object)
    
    for row in contract_info_one_month.itertuples():
        row_index = getattr(row, 'Index')
        available_ads_index = get_available_ads_index(
            row_index,
            getattr(row, 'contract_date_as_days'), 
            ad_info_one_month)
        av_df['av'].loc[row_index] = available_ads_index
    return av_df


