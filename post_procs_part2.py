import pandas as pd
import numpy as np
import json

#======================POST_PROCESSSING============================w
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

#get those two dictionary make a function with var as a variable to apply for loop over this function and 
#output should be the roi value and make a dictionary with roi values and integrate it with the final output.
#====================================================
#SAME ROI FOR THE COLUMNS MULTIPLIED (MAYBE)
#====================================================
def roi_var(last_inp,coeff,hier,var,channel_list,lr,decay,driver):
    last_copy= last_inp.copy() 
    last_copy[var]= last_copy[var]*0.9 #for 10% decrease in the value of the last_val, the change in sales are noted
    #make the transformations and check the sales
    test= user_inp_2_test(last_copy,last_inp,channel_list,lr,decay,driver) #driver for only useful values
    test['Intercept']=1
    #aligning the columns for multiplication
    test=test[coeff.columns]
    result=dict(zip((coeff[hier]),(coeff*test).sum(axis=1)))
    test_sales= result.get(spc_hier)
    last_sales= last_inp['Sales'+str('_log')].sum()
    roi=(np.exp(test_sales)-np.exp(last_sales))*100/np.exp(last_sales)
    return roi
    

def rounding_off(data):
    data={x:round(y,2) for x,y in data.items() }
    return data
def rep_zero(data,var):
    zeroes=data.index[data[var]==0].tolist()
    value=data[var].sort_values().tolist()[len(zeroes)]
    data.loc[zeroes,var]=value/100
    
def log_var_crores(data,var):
    data[var+str('_log')]=np.log(data[var])
def log_var(data,var):
    if data[var].min()==0:
        #function for that value take that index and put second min value 
        rep_zero(data,var)
        data[var+str('_log')]=np.log(data[var])
    else:
        data[var+str('_log')]=np.log(data[var])

def zeroes_finder(data):
    index=data.min().index
    values=data.min().values
    for i in range(len(index)):
        if ((index[i]=='Zone') or (index[i]=='Region')):
            pass
        if (values[i]==0):
            rep_zero(data,index[i])
          
#WITH GIVEN BUDGET, WE APPX PARAMETERS FOR MAX SALE BY SCALING DOWN RECOMMENDED VALUES              
def pred_bugdet(bugdet,rec_values):
    rec_sum=0
    for values in list(rec_values.values()):
        rec_sum+=values
    for key in list(rec_values.keys()):
        value = rec_values[key]
        value = value*bugdet/rec_sum
        rec_values[key]=value
    return rec_values
            
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
def p_chg_sales(test,last):
    change=(np.exp(test)-np.exp(last))*100/np.exp(last)
    p_changes={'per_sales':change,'appx_sales':np.exp(test)}
    #json_p_changes=json.dumps(p_changes)
    return p_changes

def p_chg_sales_recom(test,last):
    change=(np.exp(test)-np.exp(last))*100/np.exp(last)
    p_changes={'recommended_per_sales':change,'recommended_appx_sales':np.exp(test)}
    return p_changes


#variable for transformation is var lr rate is 0.1 decay is 0.69315 and defualt value for ar_coeff is 0.3
def ad_stock_s_curve_user(data,prev_data,var,lr_list,decay_list):
    ad_stock_list=[]
    ad_stock_list2=[]
#
    lr_rate=float(lr_list[var])
    decay=float(decay_list[var])
    
    ad_stock_value=prev_data[var].sum()
    ad_stock_value2=prev_data[var].sum()
    for index,row in data.iterrows():
        t=row[str(var)]
        ad_stock_value=(1/(1+np.exp(-lr_rate*t)))+ad_stock_value*decay
        ad_stock_value2=1- np.exp(-lr_rate*t)+ad_stock_value2*decay
        ad_stock_list.append(ad_stock_value)
        ad_stock_list2.append(ad_stock_value2)
        
    data['ad_stock_s_'+str(var)]=ad_stock_list
    data['ad_stock_nad_'+str(var)]=ad_stock_list2
    
    
def user_inp_2_test(user_input,last_val,channel_list,lr,decay,driver):
    df_u=pd.DataFrame.from_dict(user_input,orient='index')
    df_u=df_u.T
    user_inp_2_test.user_val=df_u
    #Converting the user input data into test data 
    for i in range(len(channel_list)):
        
        ad_stock_s_curve_user(df_u,last_val,channel_list[i],lr,decay)
        log_var_crores(df_u,str('ad_stock_nad_')+channel_list[i])
        log_var_crores(df_u,str('ad_stock_s_')+channel_list[i])
    log_var(df_u,'PCV')
    log_var(df_u,'Price')
    
    #keeping the desired variables
    df_u=df_u[driver]
    
    return df_u


def user_input_part2(data_promo1,hier,spc_hier,channel_list,model,lr,decay,config_All_india_promo,driver,data_json,mod):
    date_promo=[]
    for i in range(int(config_All_india_promo[config_All_india_promo['derived_dimension']=='date_var']['num_rav_var'].values[0])):
        date_promo.append(config_All_india_promo[config_All_india_promo['derived_dimension']=='date_var']['rv'+str(i+1)].values[0])
    
    #FETCHING THE LAST VALUE FROM A PARTICULAR BRAND 
    
    #FETCH THE LAST ZONE_REGION WISE DATA FOR ADSTOCKS -_- 
# =============================================================================
#     CHANGE THIS FUNCTION FOR THE VALUES of ADSTOCKS 
#     if mod=='Zone':
#         user_input_part2.last=data_promo1[data_promo1[hier]==spc_hier].tail(1)
# 
# =============================================================================
    user_input_part2.last=data_promo1[data_promo1[hier]==spc_hier].tail(1)
    
    user_input_part2.rem_col=list(set(list(user_input_part2.last.columns))-set([hier]+date_promo +['Sales', 'PCV', 'Price']+channel_list))
    
    user_input_part2.last_val=user_input_part2.last.drop(columns=user_input_part2.rem_col)
    user_input_part2.last_val_dict= user_input_part2.last_val.reindex().to_dict('records')
    user_input_part2.user_inp={}
    pcv_u=float(data_json['PCV'])
    Price_u=float(data_json['Price'])
    user_input_part2.user_inp['PCV']=pcv_u
    user_input_part2.user_inp['Price']=Price_u
    for i in range(len(channel_list)):
        user_input_part2.user_inp[channel_list[i]]=float(data_json[channel_list[i]])
    #keeping specified cols
    
    user_input_part2.test=user_inp_2_test(user_input_part2.user_inp,user_input_part2.last_val,channel_list,lr,decay,driver)
    user_input_part2.pred=model.predict(user_input_part2.test)
    user_input_part2.coeff_1=coeff123(data_promo1,hier,spc_hier,model)
    coeff1=user_input_part2.coeff_1.copy()
    coeff1.drop(columns=[hier],inplace=True)
    coeff1.reset_index(inplace=True,drop=True)
    user_input_part2.test['Intercept']=1
    #user_input_part2.test=user_input_part2.test.append([user_input_part2.test]*(len(data_promo1[hier].unique())-1),ignore_index=True)
    user_input_part2.test=user_input_part2.test[coeff1.columns]
    #combining both list 
    user_input_part2.result=dict(zip((user_input_part2.coeff_1[hier]),(coeff1*user_input_part2.test).sum(axis=1)))
    #user_input_part2.last.Sales.values[0]=user_input_part2.last.Sales.values[0].to_dict('index')
    #print('Last month sales: ',user_input_part2.last.Sales.values[0])
    p_sales=p_chg_sales(user_input_part2.result.get(spc_hier),user_input_part2.last['Sales'+str('_log')].sum())
    #creating a json output
    #creating a dict for best possible value 
    
    #this dict contains all the imoprtant variables like channel_list and PCV and Price with their corresponding names of variables like ad_stock and log values
    one_one_dict={}
    for i in range(len(channel_list)):
        one_one_dict[channel_list[i]]=user_input_part2.coeff_1.columns[i]
    one_one_dict['Price']='Price_log'
    one_one_dict['PCV']='PCV_log'
    one_one_dict={y:x for x,y in one_one_dict.items()}
    keep_col=list(set(data_promo1.columns)-set(user_input_part2.rem_col))
    
    last=data_promo1[keep_col].tail(len((data_promo1[hier]).unique()))
    last=last[list(one_one_dict.values())]
    
    user_input_part2.coeff_1_copy=user_input_part2.coeff_1[list(one_one_dict.keys())]
    #FINDING THE BEST VALUESs
    user_input_part2.best_values={}
    for key in one_one_dict:
        if user_input_part2.coeff_1_copy[key][0]>=0:
            user_input_part2.best_values[one_one_dict[key]]=last[one_one_dict[key]].max()
        if user_input_part2.coeff_1_copy[key][0]<0:
            user_input_part2.best_values[one_one_dict[key]]=last[one_one_dict[key]].min()
    
    #SALES of recommended values
    #THIS CHANGES IT TO ADSTOCK AND LOG TRANSFORMATION
    user_input_part2.test1=user_inp_2_test(user_input_part2.best_values,user_input_part2.last_val,channel_list,lr,decay,driver)
    user_input_part2.coeff_11=coeff123(data_promo1,hier,spc_hier,model)
    
    coeff11=user_input_part2.coeff_11.copy()
    coeff11.drop(columns=[hier],inplace=True)
    coeff11.reset_index(inplace=True,drop=True)
    user_input_part2.test1['Intercept']=1
    
    #user_input_part2.test=user_input_part2.test.append([user_input_part2.test]*(len(data_promo1[hier].unique())-1),ignore_index=True)
    user_input_part2.test1=user_input_part2.test1[coeff11.columns]
        
    #combining both list with names and values
    user_input_part2.result1=dict(zip((user_input_part2.coeff_11[hier]),(coeff11*user_input_part2.test1).sum(axis=1)))
    p_sales_recom=p_chg_sales_recom(user_input_part2.result1.get(spc_hier),user_input_part2.last['Sales'+str('_log')].sum())
    budget = float(data_json['budget'])
    budget_params = pred_bugdet(budget,user_input_part2.best_values) 
    rounding_off(p_sales)
    rounding_off(user_input_part2.best_values)
    rounding_off(p_sales_recom)
    print(rounding_off(user_input_part2.best_values))
    
    #function for roi values with for loop in new channel_list 
    roi_dict={}
    for channel in channel_list:
        roi_dict[channel] = roi_var(user_input_part2.last_val,coeff11,hier,var,channel_list,lr,decay,driver) 
        
    
    output2={'per_of_sales':rounding_off(p_sales),"recommendation":rounding_off(user_input_part2.best_values),"Recommendation_on_budget": rounding_off(budget_params),"recommended_sales":rounding_off(p_sales_recom), "ROI":rounding_off(roi_dict)}
    return output2 
    
    


