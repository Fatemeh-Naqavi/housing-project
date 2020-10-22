from statistics import NormalDist
import scipy.stats as stats
import numpy as np
import pandas as pd
from bisect import bisect_right 


def one_month_data(data_frame):
    return data_frame.loc[data_frame['contract_date_as_days'] < 643].copy() #671 for all first month

# %%

def get_available_ads_index(index_row, base_contract_date, base_contract_price, ad_info):
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
    #ad_info.loc[available_ads].sort_values(by = ['contract_price'], inplace = True)
    #available_ad_df = ad_info.loc[available_ads]#[ad_info.loc[available_ads]['contract_price'] <= base_contract_price]    
    return np.array(available_ads) 

def get_availabe_ads_new_method(contract_info_one_month, ad_info_one_month):
    av_df = pd.DataFrame(index = contract_info_one_month.index, columns = ['av']).astype(object)
    
    for row in contract_info_one_month.itertuples():
        row_index = getattr(row, 'Index')
        available_ads_index = get_available_ads_index(
            row_index,
            getattr(row, 'contract_date_as_days'), 
            getattr(row, 'contract_price'),
            ad_info_one_month)
        av_df['av'].loc[row_index] = available_ads_index
    return av_df


def get_next_larger_price(ad_price_series_sorted, base_price):
    next_larger_price = ad_price_series_sorted[bisect_right(ad_price_series_sorted, base_price)]
    return next_larger_price
    
def add_next_larger_price_to_ad_info(ad_info):
    ad_sorted_price = ad_info.contract_price.sort_values().tolist()
    larger_price = pd.Series(index =ad_info.index)
    for i, item in enumerate(ad_info['contract_price']):   
        if i < len(ad_info['contract_price']) -1 :
            larger_price.loc[ad_info.index[i]] = get_next_larger_price(ad_sorted_price, item)
        else: larger_price.loc[ad_info.index[i]] = ad_info['contract_price'].loc[ad_info.index[i]]
    ad_info['larger_price'] = larger_price
    return ad_info
    
    
def get_dif_cdf_for_prices(lower_price, upper_price,beta):
    cdf_low = get_cdf(lower_price,beta)
    cdf_up = get_cdf(upper_price,beta)
    cdf = cdf_up - cdf_low
    return  cdf

def get_cdf1(price,beta):
    mu1 = beta[2]
    B = beta[3]*beta[3]
    cdf = stats.gumbel_r.cdf(price, mu1, B)
    return cdf

def get_cdf(price,beta):
    mu1 = beta[2]
    sigma1 = beta[3]*beta[3]
    cdf = NormalDist(mu=mu1, sigma=sigma1).cdf(price)
    return cdf


def get_last_dif_cdf(price):
    cdf_low = get_cdf(price)
    cdf_up = 1
    cdf = cdf_up - cdf_low
    return  cdf