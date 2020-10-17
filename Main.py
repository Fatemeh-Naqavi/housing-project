import numpy as np
import pandas as pd
import scipy.optimize as op
import Model 
import DataPrep

# %%
ad_info_one_month = pd.read_csv('OneMonthData.csv', index_col='Index')
contract_info_one_month = DataPrep.one_month_data(ad_info_one_month)
ad_info_one_month['living_area'] = ad_info_one_month['living_area'].apply(lambda x: np.log(x))
ad_info_one_month['contract_price'] = ad_info_one_month['contract_price'].apply(lambda x: (x/1000000))
contract_info_one_month['contract_price'] = contract_info_one_month['contract_price'].apply(lambda x: np.log(x))
contract_info_one_month = DataPrep.add_next_larger_price_to_contract_info(contract_info_one_month, ad_info_one_month)
all_av_ad_df = DataPrep.get_availabe_ads_new_method(contract_info_one_month, ad_info_one_month)

# %%
def log_likelihood(beta):
    prb = Model.calculate_prob(contract_info_one_month, ad_info_one_month, all_av_ad_df, beta)
    ll = -np.sum(np.log(prb))
    print(ll)
    return ll


#beta = np.array([[-0.03 , 62, 15 ,1.2]])
beta = np.array([[1] , [2], [3] ,[2]])
beta1 = np.array([[0.05] , [5], [1.2] ,[2]])
result = op.minimize(log_likelihood, beta, method='CG')

print(result)
