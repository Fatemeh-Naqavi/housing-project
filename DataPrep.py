import pandas as pd



def convert_date_to_days_from_first_published_ad_date(contract_date_series, published_ad_date_series):
    first_published_add_date = published_ad_date_series.min()
    first_published_add_date - published_ad_date_series[0]
    new_contract_date_series = contract_date_series.apply(
        lambda x: (x - first_published_add_date).days)
    new_published_ad_date_series = published_ad_date_series.apply(
        lambda x: (x - first_published_add_date).days)

    return new_contract_date_series, new_published_ad_date_series

# %%

def one_month_data(data_frame):
    return data_frame.loc[data_frame['contract_date_as_days'] < 643]

# %%
def get_available_ads(index_row, base_contract_date, ad_info):
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