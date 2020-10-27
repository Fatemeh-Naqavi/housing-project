import numpy as np
import pandas as pd
import DataPrep1


def get_utility(av_ad_array, contract_info_one_month, ad_info_one_month, beta, index_row,av_ads):
    
    first = beta[0]*av_ad_array[:,2]
    utility_array = first
    duplicateIndicator = add_duplicate_indicator(utility_array, av_ad_array)
    dif_cdf = []
    for i in range(len(av_ad_array)):
        if(i != len(av_ad_array)):
            index = av_ad_array[i,0].astype(int)
            mask = av_ads[:, 0] == index
            larger_price = av_ads[mask, 1]
            dif_cdf.append(DataPrep1.get_dif_cdf_for_prices(av_ad_array[i,1],larger_price[0] ,beta))
        else:
            dif_cdf.append(DataPrep1.get_last_dif_cdf(av_ad_array[i,1]))
    #X = np.reshape(utility_array,(1, utility_array.size))
    utility_df = pd.DataFrame(utility_array, index  =  av_ad_array[:,0].astype(int) ,columns=['utility'])  
    utility_df['dif_cdf'] = dif_cdf
    utility_df['duplicateIndicator'] = duplicateIndicator
    utility_df['larger_prices'] = av_ad_array[:,1]
    utility_df.reset_index(inplace = True)
    
    utility_array = np.array(utility_df)
    return utility_array

def add_duplicate_indicator(utility_array, av_ad_array):
    av_ad_series = pd.Series(av_ad_array[:,1],index = av_ad_array[:,0])
    duplicateIndicator = av_ad_series.duplicated(keep='last')            
    return np.array(duplicateIndicator)
    
def get_probability(utility_array,row_index):
    #prob_df = pd.DataFrame(index = utility_df.index)
    du=np.max(utility_array[:,1])
    utility_normalized = utility_array[:,1] - du
    exp_utility = []
    for i in range (len(utility_normalized)):
        exp_utility.append(np.exp(utility_normalized[i]))
    exp_utility = np.array(exp_utility)
    #exp_utility = np.exp(utility_normalized)
    cumsum_exp_utility = np.cumsum(exp_utility)
    dup_indicator = utility_array[:,3]
    cumsum_exp_utility[dup_indicator.tolist()]= np.nan
    cumsum_exp_utility = np.array(pd.Series(cumsum_exp_utility).fillna(method = 'bfill'))    
    mask = utility_array[:, 0] == row_index
    Pij = exp_utility[mask]/cumsum_exp_utility
    dcdf_Pij = Pij*utility_array[:,2]
    
    #prob_df['exp_utility'] = utility_df['utility'] - du#.apply(lambda x: np.exp(x-du))
    #prob_df['cumsum_exp_utility'] = np.cumsum(prob_df['exp_utility'])
    #prob_df['dup_indicator'] = utility_df['dup_indicator']
    #prob_df['cumsum_exp_utility'].loc[utility_df['dup_indicator']]=None
    #prob_df['cumsum_exp_utility'] = prob_df['cumsum_exp_utility'].fillna(method = 'bfill')
    #prob_df['dif_cdf'] = utility_df['dif_cdf']
    #prob_df['Pij'] = prob_df['exp_utility'].loc[row_index]/prob_df['cumsum_exp_utility']
    #prob_df['dcdf*Pij'] = prob_df['Pij']*prob_df['dif_cdf']
    
    return dcdf_Pij
    

def calculate_prob(ad_info_array, contract_info_array, beta): 
    prob = pd.Series()
    prob = prob.reindex(contract_info_array[:,0])
    #for i, item in enumerate(contract_info_one_month['zone']):
    for i in range(len(prob)):
        index_row = contract_info_array[i,0]
        base_contract_price = contract_info_array[i,1]         
        av_ads = pd.DataFrame(contract_info_array[i,6][0])
        av_ads.reset_index(inplace = True)
        av_ads = np.array(av_ads) 
        av_ads = av_ads[~np.isnan(av_ads).any(axis=1)]
        av_ad_indeces = av_ads[:,0].astype(int)

        #av_ads.dropna(axis=0, inplace=True)
        #av_ad_indeces = np.array(av_ads.index)
        #av_ad_larger_prices = av_ads[:,1]     
        av_ad_array = ad_info_array[np.isin(ad_info_array[:,0],av_ad_indeces)]        
        av_ad_array = av_ad_array[av_ad_array[:,1].argsort()]
        #av_ad_df['larger_prices'] = av_ads
        bool_lower_prices = (av_ad_array[:,1]< base_contract_price)
        #lower_prices = av_ad_array[bool_lower_prices]
        #lower_prices_index = lower_prices[:,0]
        utility = get_utility(av_ad_array, contract_info_array,ad_info_array, beta, index_row,av_ads)
        #prob_serie = get_probability(utility,index_row)
        dcdf_Pij = get_probability(utility,index_row)
        dcdf_Pij[bool_lower_prices] = 0
        #prob_serie['dcdf*Pij'].loc[lower_prices_index] = 0      
        #prob.loc[index_row] = sum(prob_serie['dcdf*Pij'])
        prob.loc[index_row] = sum(dcdf_Pij)
    return prob


