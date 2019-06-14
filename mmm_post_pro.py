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

def rounding_off(data):
    data={x:round(y,2) for x,y in data.items() if type(y) != str}
    return data

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
def user_input(data_promo1,hier,spc_hier,channel_list,model,lr,decay,config_All_india_promo,driver,data_json):
    date_promo=[]
    for i in range(int(config_All_india_promo[config_All_india_promo['derived_dimension']=='date_var']['num_rav_var'].values[0])):
        date_promo.append(config_All_india_promo[config_All_india_promo['derived_dimension']=='date_var']['rv'+str(i+1)].values[0])
    
    user_input.last=data_promo1[data_promo1[hier]==spc_hier].tail(1)
    
    user_input.rem_col=list(set(list(user_input.last.columns))-set([hier]+date_promo +['Sales', 'PCV', 'Price']+channel_list))
    
    user_input.last_val=user_input.last.drop(columns=user_input.rem_col)
    user_input.last_val_dict= user_input.last_val.reindex().to_dict('records')

    user_input.coeff_1=coeff123(data_promo1,hier,spc_hier,model)
    user_input.coeff_1_user=user_input.coeff_1.to_dict('records')
# =============================================================================
#     rounding_off(user_input.last_val_dict)
#     rounding_off(user_input.coeff_1_user)
# =============================================================================
    output={'last_param':rounding_off(user_input.last_val_dict[0]),'coeff':rounding_off(user_input.coeff_1_user[0])}

    return output
    
    


