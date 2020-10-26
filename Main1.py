import numpy as np
import pandas as pd
import scipy.optimize as op
import Model1
import DataPrep1

# %%
#contract_info_one_month = pd.read_csv('contract_info_one_month_with_zone_and_larger_prices.csv', index_col='Unnamed: 0')
ad_info_one_month = pd.read_csv('ad_info_one_month_Stockholm.csv',index_col = 'Unnamed: 0')
#larger_prices = pd.read_csv('larger_prices_av_ad.csv',delimiter=())



contract_info_one_month = pd.read_pickle('./contract_info_one_month.pkl')
contract_info_one_month = DataPrep1.one_month_data(contract_info_one_month)

ad_info_one_month['living_area'] = ad_info_one_month['living_area'].apply(lambda x: np.log(x))
ad_info_one_month['contract_price'] = 1/1000000*ad_info_one_month['contract_price']#.apply(lambda x: (x/1000000))
contract_info_one_month['living_area'] = contract_info_one_month['living_area'].apply(lambda x: np.log(x))

# %%
def log_likelihood(beta):
    prb = Model1.calculate_prob(ad_info_one_month, contract_info_one_month, beta)
    ll = -sum(np.log(prb))
    print(beta)
    print(ll)
    return ll



# = np.array([[-0.45314805] , [-0.00438143], [1.2] ,[2]])
#beta = np.array([-0.45314805,  -0.00438143, -3.75877780e+00,  2.25308166e+00])
#beta = np.array([-0.70704267, 203.11556764,   1.82611619,  -1.01439868])

# beta = np.array([-0.70704267, 2.11556764,   1.82611619,  -1.01439868])
# beta = np.array([-0.45314805,  -0.00438143,   1.82611619,  1.01439868])
# beta = np.array([-1.24528573e+00,  2.34835448e-01,  1.30935710e+01,  8.27304970e-03])
# beta = np.array([-0.45314805, -0.00438143,  1.30935710e+01,  8.27304970e-03])
# beta = np.array([ 0.03589658, 2.76530047, 2.17721526, 1.00960208])
# beta = np.array([ -0.16290547,  3.34445335,  2.13655182,  1.01052149])
# beta = np.array([-0.08675873,  3.62659009,  2.07862326,  1.01044824])
beta = np.array([0.38943141, 3.82960136, 0.66704778])


#beta = np.array([[ 6.74721728e+00,  3.17074577e+03, -3.75877780e+00,  2.25308166e+00]])


result = op.minimize(log_likelihood, beta, method='BFGS',options={'maxiter':100})

print(result)

