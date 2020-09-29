import numpy as np
import pandas as pd
import scipy.optimize as op
import Model 

import DataPrep

# %%
data = DataPrep.get_default_date()

(new_contract_date_series, new_published_ad_date_series) = DataPrep.convert_date_to_days_from_first_published_ad_date(
    data['contract_date'],
    data['ad_publicized_date']
)

one_month_ads = data.loc[data['ad_publicized_date'] < '2005-02-01'].sort_values('ad_publicized_date')
one_month_contracts = data.loc[data['contract_date'] < '2005-02-01'].sort_values('contract_date')

ad_info_one_month = pd.DataFrame({
    'contract_date_as_days': new_contract_date_series,
    'ad_published_date_as_days': new_published_ad_date_series,
    'living_area': one_month_ads['living_area'],
    'contract_price': one_month_ads['contract_price']
}, index=one_month_ads.index)

contract_info_one_month = DataPrep.one_month_data(ad_info_one_month)

ad_info_one_month['living_area'] = ad_info_one_month['living_area'].apply(lambda x: np.log(x))
ad_info_one_month['contract_price'] = ad_info_one_month['contract_price'].apply(lambda x: np.log(x))

# %%
def log_likelihood(beta):
    prb = Model.calculate_prob(contract_info_one_month, ad_info_one_month, beta)
    ll = -np.sum(np.log(prb))
    return ll


beta = np.array([[1 , 1]])
result = op.minimize(log_likelihood, beta, method='CG')

print(result)
