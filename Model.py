import numpy as np
import scipy.optimize as op

import DataPrep


def get_utility(available_ad_data_frame, beta):
    first = available_ad_data_frame['living_area'].apply(lambda x: x * beta[0])
    second = available_ad_data_frame['contract_price'].apply(lambda x: x * beta[1])
    utility = first + second
    return utility


def get_probability(utility):
    prob = np.exp(utility) / sum(np.exp(utility))
    return prob


def calculate_prob(contract_info_one_month, ad_info_one_month, beta):
    contract_info_one_month['prob'] = 0
    for i, item in enumerate(contract_info_one_month['contract_date_as_days']):
        index_row = contract_info_one_month.index[i]
        available_ad_list = DataPrep.get_available_ads(index_row, item, ad_info_one_month)
        available_ad_data_frame = ad_info_one_month.loc[available_ad_list]
        utility = get_utility(available_ad_data_frame, beta)
        prob_serie = get_probability(utility)
        contract_info_one_month['prob'].loc[index_row] = prob_serie.loc[index_row]
    return contract_info_one_month['prob']
