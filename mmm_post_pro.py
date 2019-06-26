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
    for i in chann_list:
        vol[i]= (data_promo1[data_promo1[hier]==spc_hier][str('ad_stock_nad_')+str(i)].sum())*coeff_1_user[0][str('ad_stock_nad_')+str(i)]/t_sales
    for j in range(4): 
        vol[str('season_')+str(j)]=(data_promo1[data_promo1[hier]==spc_hier][str('season_')+str(j)].sum())*coeff_1_user[0][str('season_')+str(j)]/t_sales
    vol['Price']=(data_promo1[data_promo1[hier]==spc_hier]['Price'].sum())*coeff_1_user[0]['Price']/t_sales
    vol['PCV']=(data_promo1[data_promo1[hier]==spc_hier]['PCV'].sum())*coeff_1_user[0]['PCV']/t_sales
    vol['Base_sales']= len(data_promo1[data_promo1[hier]==spc_hier]['PCV'])*coeff_1_user[0]['Intercept']/t_sales
    return vol 

#SINCE WE HAVE FEWER COLUMNS LEFT BECAUSE OF CORRELATION WE ShOW THE LEFT ONES AS COMBINATION 
def vol_combo(added_col1,added_col2):
    local_var  = {} 
    for i in range(len(added_col1)):
        if added_col1[i] in local_var:
            if added_col2[i] in local_var:
                local_var[added_col1[i]] = str(local_var[added_col1[i]]) + str('*') + str(local_var[added_col2[i]])
                local_var.pop(added_col2[i])
            else :
                local_var[added_col1[i]] = str(local_var[added_col1[i]]) + str('*') + str(added_col2[i])
        else :
            local_var[added_col1[i]] = str(added_col1[i])+str('*')+ str(added_col2[i])
    return local_var

def rounding_off(data):
    data={x:round(y,2) for x,y in data.items() if type(y) != str}
    return data

# =============================================================================
# def rounding_off(data):
#     data={x:round(y,2) for x,y in data.items() if ((type(y) == float) or (type(y)==int)) }
#     return data
# =============================================================================
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
    
    last=data_promo1[data_promo1[hier]==spc_hier].tail(1)
    #Chann list contain original channel_list no the revised one 
    rem_col=list(set(list(last.columns))-set([hier]+date_promo +['Sales', 'PCV', 'Price']+chann_list+[str('season_')+str(i) for i in range(4)]))
    
    last_val=last.drop(columns=rem_col)
    last_val_dict= last_val.reindex().to_dict('records')
    
    coeff_1=coeff123(data_promo1,hier,spc_hier,Model.mdf1_sea) 
    coeff_1_user=coeff_1.to_dict('records') 
    
    #CREATING A VOLUME DISTRIBUTION BAR CHART (CONTRIBUTION) 
    vol_dist=vol_distr(data_promo1,hier,spc_hier,chann_list,coeff_1_user)
    vol_local= vol_combo(added_col1,added_col2)
    for i in chann_list:
        vol_dist[vol_local[i]]=vol_dist.pop(i)
# =============================================================================
#     rounding_off(last_val_dict)
#     rounding_off(coeff_1_user)
# =============================================================================
        
    output={'last_param':rounding_off(last_val_dict[0]),'coeff':rounding_off(coeff_1_user[0]),'Vol_distribution':rounding_off(vol_dist)}

    return output
    
    


