import numpy as np
import pandas as pd



def get_utility(available_ad_data_frame, beta):
    #first = available_ad_data_frame['living_area'].apply(lambda x: x * beta[0])
    first = available_ad_data_frame['living_area'].apply(lambda x: x * 0)
    second = 0 # available_ad_data_frame['contract_price'].apply(lambda x: x * beta[1])
    utility = first + second
    return utility


def get_probability(utility):
    prob = np.exp(utility) / sum(np.exp(utility))
    return prob

def get_probabilitymask(utility,mask):
    prob = np.exp(utility) / sum(np.exp(utility[mask]))
    prob[~(mask)]=0;
    return prob

def calculate_prob(contract_info_one_month, ad_info_one_month, beta):
    
    prob = pd.Series()
    prob = prob.reindex(contract_info_one_month.index)
    probpoor=prob.copy()
    probmed=prob.copy()
    for i, item in enumerate(contract_info_one_month['contract_date_as_days']):
        index_row = contract_info_one_month.index[i]
        av_ad_series = pd.Series(contract_info_one_month['larger_prices_av_ad'][index_row][0])        #av_ad_array = ad_info_one_month[np.isin(ad_info_array[:,0],av_ad_indeces)] 
        av_ad_df = ad_info_one_month.loc[ad_info_one_month.index.isin(av_ad_series.index)]
        mask = av_ad_df['contract_price'] <2  
        mask2 = av_ad_df['contract_price'] < 1        

        utility = get_utility(av_ad_df, beta)
        prob_serie = get_probability(utility)   
        prob.loc[index_row] = prob_serie.loc[index_row].copy()
        prob_seriepoor = get_probabilitymask(utility,mask2)   
        probpoor.loc[index_row] = prob_seriepoor.loc[index_row].copy()
        prob_seriemed = get_probabilitymask(utility,mask)   
        probmed.loc[index_row] = prob_seriemed.loc[index_row].copy()
#        Ppoor= NormalDist(mu=beta[1], sigma=beta[2]).cdf(1)
#        Pmed= NormalDist(mu=beta[1], sigma=beta[2]).cdf(2)-Ppoor
#    return (1-Ppoor-Pmed)*prob+Ppoor*probpoor+Pmed*probmed
    print(beta)
    return (1-abs(beta[0]))*prob+abs(beta[0])*probmed
