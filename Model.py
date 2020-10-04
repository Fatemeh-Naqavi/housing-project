import numpy as np
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
    contract_info_one_month.loc[:,'prob'] = 0
    for i, item in enumerate(contract_info_one_month['contract_date_as_days']):
        index_row = contract_info_one_month.index[i]
        base_contract_price = contract_info_one_month['contract_price'].loc[index_row]
        available_ad_df = DataPrep.get_available_ads(index_row, item, base_contract_price, ad_info_one_month)  
        utility = get_utility(available_ad_df, beta)
        prob_serie = get_probability(utility)       
        if(i != len(contract_info_one_month)):
            dif_cdf = DataPrep.get_dif_cdf(ad_info_one_month['contract_price'],index_row)
        else:
            dif_cdf = DataPrep.get_last_dif_cdf(base_contract_price)
        print("I : ", i, "CDF: ", dif_cdf, "Length: ", len(available_ad_df))
        contract_info_one_month['prob'].loc[index_row] = prob_serie.loc[index_row] * dif_cdf
    return contract_info_one_month['prob']
