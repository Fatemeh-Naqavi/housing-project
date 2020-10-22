import numpy as np
import pandas as pd
import DataPrep


def get_utility(available_ad_data_frame, beta):
    available_ad_data_frame.sort_values(by = ['contract_price'], inplace = True)
    first = available_ad_data_frame['living_area'].apply(lambda x: x * beta[0])
    second = available_ad_data_frame['contract_price'].apply(lambda x: x * beta[1])
    utility_serie = first + second
    utility_df = add_duplicate_indicator(utility_serie, available_ad_data_frame)
    dif_cdf = pd.Series(index = available_ad_data_frame['larger_price'].index)
    for i, row in available_ad_data_frame.iterrows():
        if(i != len(available_ad_data_frame)):
            dif_cdf[row.name] = DataPrep.get_dif_cdf_for_prices(row['contract_price'],row['larger_price'],beta)
        else:
            dif_cdf[row.name] = DataPrep.get_last_dif_cdf(row['contract_price'])
    utility_df['dif_cdf'] = dif_cdf
    return utility_df

def add_duplicate_indicator(utility_serie, available_ad_data_frame):
    duplicateIndicator = available_ad_data_frame['contract_price'].duplicated(keep='last')            
    utility_df = pd.DataFrame({ 'utility': utility_serie, 'dup_indicator': duplicateIndicator } )
    return utility_df
            
    
def get_probability(utility_df,row_index):
    prob_df = pd.DataFrame(index = utility_df.index)
    prob_df['exp_utility'] = utility_df['utility'].apply(lambda x: np.exp(x))
    prob_df['cumsum_exp_utility'] = np.cumsum(prob_df['exp_utility'])
    prob_df['dup_indicator'] = utility_df['dup_indicator']
    prob_df['cumsum_exp_utility'].loc[utility_df['dup_indicator']]=None
    prob_df['cumsum_exp_utility'] = prob_df['cumsum_exp_utility'].fillna(method = 'bfill')
    prob_df['dif_cdf'] = utility_df['dif_cdf']
    prob_df['Pij'] = prob_df['exp_utility'].loc[row_index]/prob_df['cumsum_exp_utility']
    prob_df['dcdf*Pij'] = prob_df['Pij']*prob_df['dif_cdf']
    
    return prob_df
    

def calculate_prob(contract_info_one_month, ad_info_one_month, all_av_ad_df,beta): 
    prob = pd.Series()
    prob = prob.reindex(contract_info_one_month.index)
    for i, item in enumerate(contract_info_one_month['contract_date_as_days']):
        index_row = contract_info_one_month.index[i]
        base_contract_price = contract_info_one_month['contract_price'].loc[index_row]
        av_ad_index_array = all_av_ad_df.loc[index_row]['av']
        av_ad_df = ad_info_one_month.loc[ad_info_one_month.index.isin(av_ad_index_array)]
        lower_prices = av_ad_df.loc[av_ad_df['contract_price']< base_contract_price]
        lower_prices_index= lower_prices.index
        #av_ad_df.sort_values(by = ['contract_price'], inplace = True)
        utility = get_utility(av_ad_df, beta)
        prob_serie = get_probability(utility,index_row)
        prob_serie['dcdf*Pij'].loc[lower_prices_index] = 0      
        prob.loc[index_row] = sum(prob_serie['dcdf*Pij'])
    return prob
