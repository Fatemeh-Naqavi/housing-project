import numpy as np
import pandas as pd
import scipy.optimize as op
import Model 
import DataPrep

# %%
ad_info_one_month = pd.read_csv('OneMonthData.csv', index_col='Index')
contract_info_one_month = DataPrep.one_month_data(ad_info_one_month)
ad_info_one_month['living_area'] = ad_info_one_month['living_area'].apply(lambda x: np.log(x))
ad_info_one_month['contract_price'] = ad_info_one_month['contract_price'].apply(lambda x: np.log(x))
contract_info_one_month['contract_price'] = contract_info_one_month['contract_price'].apply(lambda x: np.log(x))

# %%
def log_likelihood(beta):
    prb = Model.calculate_prob(contract_info_one_month, ad_info_one_month, beta)
    ll = -np.sum(np.log(prb))
    print(ll)
    return ll


#beta = np.array([[-0.03 , 62, 15 ,1.2]])
beta = np.array([[2.49] , [61.10], [13.72] ,[0.73]])
result = op.minimize(log_likelihood, beta, method='CG')

print(result)
