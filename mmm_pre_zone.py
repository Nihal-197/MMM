import pandas as pd
import numpy as np

def ad_stock_s_curve_u(data,var,lr_list,decay_list):
    ad_stock_list=[]
    ad_stock_list2=[]
    
    lr_rate=float(lr_list[var])
    decay=float(decay_list[var])
    ad_stock_value=0
    ad_stock_value2=0
    for index,row in data.iterrows():
        t=row[str(var)]
        ad_stock_value=(1/(1+np.exp(-lr_rate*t)))+ad_stock_value*decay
        ad_stock_value2=1- np.exp(-lr_rate*t)+ad_stock_value2*decay
        ad_stock_list.append(ad_stock_value)
        ad_stock_list2.append(ad_stock_value2)
    data['ad_stock_s_'+str(var)]=ad_stock_list
    data['ad_stock_nad_'+str(var)]=ad_stock_list2
        #data['ad_stock_l_'+str(var)]=tsa.filters.filtertools.recursive_filter(data[var],ar_coeff)
def col_drop(hier,hier_list):
    col_2_drop=[]
    j=0
    for i in hier_list:
        j+=1
        if (i==hier):
            col_2_drop=hier_list[j:]
        
    return col_2_drop 
#Now some values can contain 0 values for log function hence finding index of them and replacing them with the second
#min value
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
def filling_na(data,hier,zone_list,channel_list):
    for_na=data.groupby(by=[hier]+zone_list).mean()
    for_na.reset_index(inplace=True)
    data.fillna(value=(-9999),inplace=True)
    for index,row  in data.iterrows():
        for promo in channel_list:
            if row[promo]==float(-9999):
                subbrand_promo=row[hier]
                zone_promo1=row[zone_list[0]]
                zone_promo2=row[zone_list[1]]
                spend_promo=for_na[(for_na[hier]==subbrand_promo) & (for_na[zone_list[0]]==zone_promo1) & 
                                   (for_na[zone_list[1]]==zone_promo2)][promo].sum()
                data.loc[index,promo]=spend_promo
def pre1(test_data_all,data_promo,config_All_india_HFD,config_All_india_promo,hier,spc_hier):
#for brand drop subbrand, for manuf. drop band and subbrand 
    pre1.hier_list = []
    for i in range(config_All_india_HFD[config_All_india_HFD['derived_dimension']=='target_dim']['num_rav_var'].sum()):
        pre1.hier_list.append(config_All_india_HFD[config_All_india_HFD['derived_dimension']=='target_dim']['rv'+str(i+1)].sum())
    pre1.date_HFD=[]
    for i in range(config_All_india_HFD[config_All_india_HFD['derived_dimension']=='date_var']['num_rav_var'].values[0]):
        pre1.date_HFD.append(config_All_india_HFD[config_All_india_HFD['derived_dimension']=='date_var']['rv'+str(i+1)].values[0])

    pre1.date_promo=[]
    for i in range(int(config_All_india_promo[config_All_india_promo['derived_dimension']=='date_var']['num_rav_var'].values[0])):
        pre1.date_promo.append(config_All_india_promo[config_All_india_promo['derived_dimension']=='date_var']['rv'+str(i+1)].values[0])

    #creating a Price column
    p_config=config_All_india_promo[config_All_india_promo['derived_dimension']=='Price']
    #applying for multivariables the pandas eval for finding the values of the Price and specs
    a_dict = {}
    for i in range(int(p_config['num_rav_var'].sum())):
        a_dict[p_config['rv'+str(i+1)].sum()]='rv'+str(i+1)
    a=test_data_all.rename(columns=a_dict).eval(p_config['formula'])
    test_data_all['Price']=a[0]*1000
    test_data_all.drop(columns=col_drop(hier,pre1.hier_list),inplace=True)

    #SPENDS=config_All_india_promo[config_All_india_promo['derived_dimension']=='Spends']['rv'+str(1)].values[0]
    PCV=config_All_india_promo[config_All_india_promo['derived_dimension']=='PCV']['rv'+str(1)].values[0]
    SALES=config_All_india_promo[config_All_india_promo['derived_dimension']=='Sales']['rv'+str(1)].values[0]
    pre1.zone_reg_col=[] 
    for i in range(2):
            pre1.zone_reg_col.append(config_All_india_promo[config_All_india_promo['derived_dimension']=='geo_level']['rv'+str(i+1)].values[0])

    #Below is the code if config file contain the column names of the spends as different columns
    pre1.channel_list=[]
    for i in range(int((config_All_india_promo[config_All_india_promo['derived_dimension']=='promotion']['num_rav_var'].sum()))):
        pre1.channel_list.append(config_All_india_promo[config_All_india_promo['derived_dimension']=='promotion']['rv'+str(i+1)].sum())

    pre1.lr={}
    pre1.decay={}
    for i in range(len(config_All_india_promo[config_All_india_promo['derived_dimension']=='Learning Rates']['num_rav_var'].sum())):
        pre1.lr[channel_list[i]]=config_All_india_promo[config_All_india_promo['derived_dimension']=='Learning Rates']['rv'+str(i+1)].sum()
        pre1.decay[channel_list[i]]=config_All_india_promo[config_All_india_promo['derived_dimension']=='Decay Rates']['rv'+str(i+1)].sum()

    #treating outliers in the model removing the values over 99%
    filling_na(data_promo,pre1.hier_list[2],pre1.zone_reg_col,pre1.channel_list)

    list_d_hier=list(pre1.date_promo)+pre1.hier_list[0:3]+pre1.zone_reg_col#list containing [Month,Manufacture,Brand,Subbrand,Zone,Region]
    data_promo_2=data_promo.groupby(by=list(set(list_d_hier)-set(col_drop(hier,pre1.hier_list)))).sum().reset_index()
    data_promo1= pd.merge(test_data_all,data_promo_2, on =list(set(list_d_hier)-set(list(col_drop(hier,pre1.hier_list)))),how='left')
    data_promo1.rename(columns={SALES:'Sales',PCV:'PCV'},inplace=True)

    #columns not to drop(non promo,sales,promo(nad stock),date)
    non_promo_col=['Price','PCV']
    non_drop_col=list(pre1.date_promo)+[hier]+list(pre1.channel_list)+['Sales']+non_promo_col

    #droppping other columns
    data_promo1.drop(columns=list(set(list(data_promo1.columns))-set(non_drop_col)),inplace=True)

    #replacing any nan due to division for taking log later
    mean=data_promo1['Price'].mean()
    data_promo1['Price'].fillna(mean,inplace=True)
    data_promo1.Price.replace(to_replace={0.0:mean},inplace=True)
    #a=zeroes_finder(data_promo1)
    rep_zero(data_promo1,'PCV')

    for i in (pre1.channel_list):
        ad_stock_s_curve_u(data_promo1,i,pre1.lr,pre1.decay)
        log_var_crores(data_promo1,str('ad_stock_nad_')+i)
        log_var_crores(data_promo1,str('ad_stock_s_')+i)
    log_var(data_promo1,'Sales')
    log_var(data_promo1,'PCV')
    log_var(data_promo1,'Price')
    return data_promo1



