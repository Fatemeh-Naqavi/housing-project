import numpy as np
import pandas as pd
import DataPrep1


def get_utility(av_ad_df, contract_info_one_month, ad_info_one_month, beta, index_row):
    
    index = av_ad_df.index
    first = beta[0]*ad_info_one_month['living_area'].loc[index]#.apply(lambda x: x * beta[0])
   # second = available_ad_data_frame['contract_price'].apply(lambda x: x * beta[1])
    utility_serie = first #+ second
    utility_df = add_duplicate_indicator(utility_serie, av_ad_df)
    dif_cdf = pd.Series(index = index)
    for i, row in ad_info_one_month.loc[index].iterrows():
        if(i != len(av_ad_df)):
            dif_cdf[row.name] = DataPrep1.get_dif_cdf_for_prices(row['contract_price'],av_ad_df['larger_prices'].loc[i],beta)
        else:
            dif_cdf[row.name] = DataPrep1.get_last_dif_cdf(row['contract_price'])
    utility_df['dif_cdf'] = dif_cdf
    return utility_df

def add_duplicate_indicator(utility_serie, av_ad_df):
    duplicateIndicator = av_ad_df['contract_price'].duplicated(keep='last')            
    utility_df = pd.DataFrame({ 'utility': utility_serie, 'dup_indicator': duplicateIndicator } )
    return utility_df
            
    
def get_probability(utility_df,row_index):
    prob_df = pd.DataFrame(index = utility_df.index)
    du=np.max(utility_df['utility'])
    prob_df['exp_utility'] = utility_df['utility'].apply(lambda x: np.exp(x-du))
    prob_df['cumsum_exp_utility'] = np.cumsum(prob_df['exp_utility'])
    prob_df['dup_indicator'] = utility_df['dup_indicator']
    prob_df['cumsum_exp_utility'].loc[utility_df['dup_indicator']]=None
    prob_df['cumsum_exp_utility'] = prob_df['cumsum_exp_utility'].fillna(method = 'bfill')
    prob_df['dif_cdf'] = utility_df['dif_cdf']
    prob_df['Pij'] = prob_df['exp_utility'].loc[row_index]/prob_df['cumsum_exp_utility']
    prob_df['dcdf*Pij'] = prob_df['Pij']*prob_df['dif_cdf']
    
    return prob_df
    

def calculate_prob(ad_info_one_month, contract_info_one_month, beta): 
    prob = pd.Series()
    prob = prob.reindex(contract_info_one_month.index)
    for i, item in enumerate(contract_info_one_month['zone']):
        index_row = contract_info_one_month.index[i]
        base_contract_price = contract_info_one_month['contract_price'].loc[index_row]   
        #x = contract_info_one_month['larger_prices_av_ad'].loc[index_row][0]
        av_ads = contract_info_one_month['larger_prices_av_ad'].loc[index_row][0]
        av_ads.dropna(axis=0, inplace=True)
        
        #row = contract_info_one_month.loc[index_row]
        
        av_ad_indeces = av_ads.index
        av_ad_df = ad_info_one_month.loc[av_ad_indeces]
        av_ad_df['larger_prices'] = av_ads
        #av_ad_df = av_ad_df.sort_values(by = ['larger_prices'])
        lower_prices = av_ad_df[av_ad_df['contract_price']< base_contract_price]
        lower_prices_index = lower_prices.index
        utility = get_utility(av_ad_df, contract_info_one_month,ad_info_one_month, beta, index_row)
        prob_serie = get_probability(utility,index_row)
        prob_serie['dcdf*Pij'].loc[lower_prices_index] = 0      
        prob.loc[index_row] = sum(prob_serie['dcdf*Pij'])
    
    return prob


