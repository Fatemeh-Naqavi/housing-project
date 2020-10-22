import numpy as np
import pandas as pd
import scipy.optimize as op
import Model 
import DataPrep

# %%
ad_info_one_month = pd.read_csv('OneMonthData.csv', index_col='Index',delimiter=';')
contract_info_one_month = DataPrep.one_month_data(ad_info_one_month)
ad_info_one_month['living_area'] = ad_info_one_month['living_area'].apply(lambda x: np.log(x))
ad_info_one_month['contract_price'] = ad_info_one_month['contract_price'].apply(lambda x: (x/1000000))
contract_info_one_month['contract_price'] = contract_info_one_month['contract_price'].apply(lambda x: (x/1000000))
#contract_info_one_month = DataPrep.add_next_larger_price_to_contract_info(contract_info_one_month, ad_info_one_month)
ad_info_one_month = DataPrep.add_next_larger_price_to_ad_info(ad_info_one_month)
ad_info_one_month = ad_info_one_month.sort_values(by = 'ad_published_date_as_days')
all_av_ad_df = DataPrep.get_availabe_ads_new_method(contract_info_one_month, ad_info_one_month)

# %%
def log_likelihood(beta):
    prb = Model.calculate_prob(contract_info_one_month, ad_info_one_month, all_av_ad_df, beta)
    ll = -np.sum(np.log(prb))
    print(beta)
    print(ll)
    return ll



# = np.array([[-0.45314805] , [-0.00438143], [1.2] ,[2]])
#beta = np.array([-0.45314805,  -0.00438143, -3.75877780e+00,  2.25308166e+00])
#beta = np.array([-0.70704267, 203.11556764,   1.82611619,  -1.01439868])
beta = np.array([-0.70704267, 2.11556764,   1.82611619,  -1.01439868])
beta = np.array([-0.45314805,  -0.00438143,   1.82611619,  1.01439868])
beta = np.array([-1.24528573e+00,  2.34835448e-01,  1.30935710e+01,  8.27304970e-03])
beta = np.array([-0.45314805, -0.00438143,  1.30935710e+01,  8.27304970e-03])
beta = np.array([ 0.03589658, 2.76530047, 2.17721526, 1.00960208])


#beta = np.array([[ 6.74721728e+00,  3.17074577e+03, -3.75877780e+00,  2.25308166e+00]])


result = op.minimize(log_likelihood, beta, method='CG',options={'maxiter':20})

print(result)


