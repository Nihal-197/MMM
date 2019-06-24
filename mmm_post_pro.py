import pandas as pd
import numpy as np
import json

#======================POST_PROCESSSING============================

#Now some values can contain 0 values for log function hence finding index of them and replacing them with the second
#min value
def col_drop(hier,hier_list):
    col_2_drop=[]
    j=0
    for i in hier_list:
        j+=1
        if (i==hier):
            col_2_drop=hier_list[j:]
    return col_2_drop
# =============================================================================
# 
# def rounding_off(data):
#     data={x:round(y,2) for x,y in data.items() if type(y) != str}
#     return data
# =============================================================================
#FUNCTION TO SUM(COLUMN OF data)*COEF/ SALES
def vol_distr(data_promo1,hier,spc_hier,chann_list,coeff_1_user):
    t_sales= data_promo1[data_promo1[hier]==spc_hier]['Sales'].sum()
    vol= {}
    #6 is added because 4=dummy_var and 2 = PCV and PRICE
    for i in chann_list:
        vol[chann_list]= data_promo1[data_promo1[hier]==spc_hier][i].sum()*coeff_1_user[i]/t_sales
    for i in range(4):
        vol[str('season_')+i]=data_promo1[data_promo1[hier]==spc_hier][i].sum()*coeff_1_user[i]/t_sales
    vol['Price']=data_promo1[data_promo1[hier]==spc_hier]['Price'].sum()*coeff_1_user['Price']/t_sales
    vol['PCV']=data_promo1[data_promo1[hier]==spc_hier]['PCV'].sum()*coeff_1_user['PCV']/t_sales
    vol['Base_sales']= len(data_promo1[data_promo1[hier]==spc_hier]['PCV'])*coeff_1_user['Intercept']/t_sales
    return vol 

def rounding_off(data):
    data={x:round(y,2) for x,y in data.items() if type(y) == float}
    return data
#getting coeficients for each brand     #data_promo1
#creating a dataframe for the coef.    
def coeff123(data_promo1,hier,spc_hier,Model):
    brands=data_promo1[hier].unique()
    ind=np.where(brands==spc_hier)
    a=Model.random_effects[brands[ind][0]].iloc[1:]+Model.fe_params.iloc[1:]
    a[hier]=brands[ind][0]
    a['Intercept']=Model.fe_params[0]
    a=a.to_frame().transpose()
    return a   
def user_input(data_promo1,hier,spc_hier,channel_list,model,lr,decay,config_All_india_promo,driver,data_json,chann_list):
    date_promo=[]
    for i in range(int(config_All_india_promo[config_All_india_promo['derived_dimension']=='date_var']['num_rav_var'].values[0])):
        date_promo.append(config_All_india_promo[config_All_india_promo['derived_dimension']=='date_var']['rv'+str(i+1)].values[0])
    
    user_input.last=data_promo1[data_promo1[hier]==spc_hier].tail(1)
    #Chann list contain original channel_list no the revised one 
    user_input.rem_col=list(set(list(user_input.last.columns))-set([hier]+date_promo +['Sales', 'PCV', 'Price']+chann_list+list(range(4))))
    
    user_input.last_val=user_input.last.drop(columns=user_input.rem_col)
    user_input.last_val_dict= user_input.last_val.reindex().to_dict('records')
    
    user_input.coeff_1=coeff123(data_promo1,hier,spc_hier,model) 
    user_input.coeff_1_user=user_input.coeff_1.to_dict('records')
    
    #CREATING A VOLUME DISTRIBUTION BAR CHART (CONTRIBUTION) 
    vol_dist=vol_distr(data_promo1,hier,spc_hier,chann_list,coeff_1_user)
    
# =============================================================================
#     rounding_off(user_input.last_val_dict)
#     rounding_off(user_input.coeff_1_user)
# =============================================================================
    output={'last_param':rounding_off(user_input.last_val_dict[0]),'coeff':rounding_off(user_input.coeff_1_user[0])}

    return output
    
    


