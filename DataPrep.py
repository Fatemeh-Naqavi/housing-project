from statistics import NormalDist
import scipy.stats as stats


def one_month_data(data_frame):
    return data_frame.loc[data_frame['contract_date_as_days'] < 643].copy() #671 for all first month

# %%
def get_available_ads(index_row, base_contract_date, base_contract_price, ad_info):
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
    ad_info.loc[available_ads].sort_values(by = ['contract_price'], inplace = True)
    available_ad_df = ad_info.loc[available_ads][ad_info.loc[available_ads]['contract_price'] <= base_contract_price]    
    return available_ad_df 

def get_dif_cdf(ad_info_series, index,beta):
    ad_info_sorted_by_price = ad_info_series.sort_values()
    ad_info_sorted_by_price_with_new_index = ad_info_sorted_by_price.reset_index()
    row = ad_info_sorted_by_price_with_new_index[ad_info_sorted_by_price_with_new_index['Index'] == index]
    lower_price = row.contract_price
    
    idx = row.index.astype(int)[0]
    upper_price_index = idx
    for i in range(idx,len(ad_info_sorted_by_price_with_new_index)):
        if (ad_info_sorted_by_price_with_new_index.contract_price.loc[i] != lower_price).bool():
            upper_price_index = i
            break
    
    upper_price = ad_info_sorted_by_price_with_new_index.loc[upper_price_index].contract_price
    return get_dif_cdf_for_prices(lower_price, upper_price,beta)

def get_dif_cdf_for_prices(lower_price, upper_price,beta):
    cdf_low = get_cdf(lower_price,beta)
    cdf_up = get_cdf(upper_price,beta)
    cdf = cdf_up - cdf_low
    return  cdf

def get_cdf(price,beta):
    mu1 = beta[2]
    if beta[3]<=0:
        beta[3] =2
    B = beta[3]
    cdf = stats.gumbel_r.cdf(price, mu1, B)
    return cdf

def get_last_dif_cdf(price):
    cdf_low = get_cdf(price)
    cdf_up = 1
    cdf = cdf_up - cdf_low
    return  cdf