import numpy as np
import pandas as pd
import DataPrep


def get_utility(available_ad_data_frame, beta):
    first = available_ad_data_frame['living_area'].apply(lambda x: x * beta[0])
    second = available_ad_data_frame['contract_price'].apply(lambda x: x * beta[1])
    utility = first + second
    return utility


def get_probability(utility):
    prob = np.exp(utility) / sum(np.exp(utility))
    return prob

def calculate_prob(contract_info_one_month, ad_info_one_month, all_av_ad_df,beta):
    
    prob = pd.Series()
    prob = prob.reindex(contract_info_one_month.index)
    for i, item in enumerate(contract_info_one_month['contract_date_as_days']):
        index_row = contract_info_one_month.index[i]
        #base_contract_price = contract_info_one_month['contract_price'].loc[index_row]
        av_ad_index_array = all_av_ad_df.loc[index_row]['av']
        av_ad_df = ad_info_one_month.loc[ad_info_one_month.index.isin(av_ad_index_array)]
        utility = get_utility(av_ad_df, beta)
        prob_serie = get_probability(utility)   
        prob.loc[index_row] = prob_serie.loc[index_row].copy()
    return prob
