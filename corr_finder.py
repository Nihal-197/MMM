import numpy as np


def corr_fin(data_promo1,channel_list):
    #converting the list into array for using it in for loop
    chann=np.array(channel_list)
    non_promo_col=np.array(['Price','PCV'])
    #correlation finder
    
    driver1=[str("ad_stock_nad_")+i for i in chann.astype('object')+ "_log"]+[j for j in non_promo_col.astype('object') + "_log"]
    driver2=[str("ad_stock_s_")+i for i in chann.astype('object')+ "_log"]+[j for j in non_promo_col.astype('object') + "_log"]

    lis1=driver1+['Sales_log']
    lis2=driver2+['Sales_log']
    
    corr1= data_promo1[data_promo1['Brand']==spc_hier][lis1].corr()
    corr2= data_promo1[data_promo1['Brand']==spc_hier][lis2].corr()
    
    for i in range(len(corr1)):
        for j in range(len(corr1)):        
            if ((corr1[lis1[i]].iloc[j])>0.8 and i>j):
                print('For NAD ad stock ','Correlation is >0.8 between',lis1[i],'and',corr1[lis1[i]].index[j])
    for i in range(len(corr2)):
        for j in range(len(corr2)):        
            if ((corr2[lis2[i]].iloc[j])>0.8 and i>j):
                print('For s curve ad stock ','correlation is >0.8 between',lis2[i],'and',corr2[lis2[i]].index[j])
        
