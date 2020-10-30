import numpy as np
import pandas as pd
import scipy.optimize as op
import Model3 
import DataPrep3

# %%

CriticalPrice=2;


ad_info_one_month = pd.read_csv('ad_info_one_month_Stockholm_apartment.csv',index_col = 'Unnamed: 0')
contract_info_one_month = pd.read_pickle('./contract_info_one_month.pkl')
contract_info_one_month = DataPrep3.one_month_data(contract_info_one_month)
ad_info_one_month['living_area'] = ad_info_one_month['living_area'].apply(lambda x: np.log(x))
ad_info_one_month['contract_price'] = ad_info_one_month['contract_price'].apply(lambda x:  (x/1000000))
#ad_info_one_month.reset_index(inplace = True)
contract_info_one_month['contract_price'] = contract_info_one_month['contract_price'].apply(lambda x:  (x))
#contract_info_one_month.reset_index(inplace = True)
contract_info_one_month['living_area'] = contract_info_one_month['living_area'].apply(lambda x: np.log(x))
# %%
def log_likelihood(beta):
    prb = Model3.calculate_prob(contract_info_one_month, ad_info_one_month, beta)
    ll = -np.sum(np.log(prb))
    print(ll)
    return ll


beta = np.array([0.3 ])#, 1])

result = op.minimize(log_likelihood, beta, method='CG')

print(result)
