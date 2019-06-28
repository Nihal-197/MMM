import pandas as pd
import numpy as np
import re
import itertools
from corr_finder import *

def log_var_crores(data,var):
    data[var+str('_log')]=np.log(data[var])
#ZONE REGION LEVEL ADSTOCK UPTO LEVEL 5 
def ad_stock_s_curve_u(data,data_promo,var,hier,spc_hier,zone_reg_col,lr_list,decay_list):
    n=len(zone_reg_col) #NUMBER OF DIFFERENT POSSIBLE ZONE/REGIONS/ANYTHING UPTO 5
    
    lr_rate=float((lr_list[var]))
    decay=float(decay_list[var]) 

    if n==2:
        a=[]
        for an in range(n):
            a.append(list(data_promo[zone_reg_col[an]].unique()))
        #a[0] CONTAINS VALUES LIKE ['North','East','West','South']
        for (x,y) in list(itertools.product(*[a[l] for l in range(n)])):
            ad_stock_value=0
            ad_stock_value2=0
            for index,row in data[(data[hier]==spc_hier) & (data[zone_reg_col[0]]==x)&(data[zone_reg_col[1]]==y)].iterrows():
                t=row[str(var)]
                ad_stock_value=(1/(1+np.exp(-lr_rate*t)))+ad_stock_value*decay
                ad_stock_value2=1- np.exp(-lr_rate*t)+ad_stock_value2*decay
                data.loc[index,'ad_stock_s_'+str(var)] =ad_stock_value
                data.loc[index,'ad_stock_nad_'+str(var)] =ad_stock_value2

    elif n==3:
        a=[]
        for an in range(n):
            a.append(list(data_promo[zone_reg_col[an]].unique()))
        for (x,y,z) in list(itertools.product(*[a[l] for l in range(n)])):
            ad_stock_value=0
            ad_stock_value2=0
            for index,row in data[(data[hier]==spc_hier) & (data[zone_reg_col[0]]==x)&(data[zone_reg_col[1]]==y) &(data[zone_reg_col[2]]==z) ].iterrows():
                t=row[str(var)]
                ad_stock_value=(1/(1+np.exp(-lr_rate*t)))+ad_stock_value*decay
                ad_stock_value2=1- np.exp(-lr_rate*t)+ad_stock_value2*decay
# =============================================================================
#                 ad_stock_list.append(ad_stock_value)
#                 ad_stock_list2.append(ad_stock_value2)
# =============================================================================
                data.loc[index,'ad_stock_s_'+str(var)] =ad_stock_value
                data.loc[index,'ad_stock_nad_'+str(var)] =ad_stock_value2
    
 
    elif n==4:
        a=[]
        for an in range(n):
            a.append(list(data_promo[zone_reg_col[an]].unique()))
        for (x,y,z,w) in list(itertools.product(*[a[l] for l in range(n)])):
            ad_stock_value=0
            ad_stock_value2=0
            for index,row in data[(data[hier]==spc_hier) & (data[zone_reg_col[0]]==x)&(data[zone_reg_col[1]]==y) &(data[zone_reg_col[2]]==z)&(data[zone_reg_col[3]]==w) ].iterrows():
                t=row[str(var)]
                ad_stock_value=(1/(1+np.exp(-lr_rate*t)))+ad_stock_value*decay
                ad_stock_value2=1- np.exp(-lr_rate*t)+ad_stock_value2*decay
# =============================================================================
#                 ad_stock_list.append(ad_stock_value)
#                 ad_stock_list2.append(ad_stock_value2)
# =============================================================================
                data.loc[index,'ad_stock_s_'+str(var)] =ad_stock_value
                data.loc[index,'ad_stock_nad_'+str(var)] =ad_stock_value2

    elif n==5:
        a=[]
        for an in range(n):
            a.append(list(data_promo[zone_reg_col[an]].unique()))
        for (x,y,z,w,u) in list(itertools.product(*[a[l] for l in range(n)])):
            ad_stock_value=0
            ad_stock_value2=0
            for index,row in data[(data[hier]==spc_hier) & (data[zone_reg_col[0]]==x)&(data[zone_reg_col[1]]==y) &(data[zone_reg_col[2]]==z)&(data[zone_reg_col[3]]==w)&(data[zone_reg_col[4]]==u) ].iterrows():
                t=row[str(var)]
                ad_stock_value=(1/(1+np.exp(-lr_rate*t)))+ad_stock_value*decay
                ad_stock_value2=1- np.exp(-lr_rate*t)+ad_stock_value2*decay
                ad_stock_list.append(ad_stock_value)
                ad_stock_list2.append(ad_stock_value2)
                data.loc[index,'ad_stock_s_'+str(var)] =ad_stock_value
                data.loc[index,'ad_stock_nad_'+str(var)] =ad_stock_value2
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
def pre1(test_data_all,data_promo,config_All_india_HFD,config_All_india_promo,hier,spc_hier,cor_coef_ad=0.7,cor_coef_else=0.8):
#for brand drop subbrand, for manuf. drop band and subbrand 
# =============================================================================
#     hier=MMM1.hier
#     spc_hier= MMM1.spc_hier
#     cor_coef_ad=0.89
#     cor_coef_else=0.8
#     #===============================DELETEEEEEE==============
    hier_list = []
    for i in range(config_All_india_HFD[config_All_india_HFD['derived_dimension']=='target_dim']['num_rav_var'].sum()):
        hier_list.append(config_All_india_HFD[config_All_india_HFD['derived_dimension']=='target_dim']['rv'+str(i+1)].sum())
    date_HFD=[]
    for i in range(config_All_india_HFD[config_All_india_HFD['derived_dimension']=='date_var']['num_rav_var'].values[0]):
        date_HFD.append(config_All_india_HFD[config_All_india_HFD['derived_dimension']=='date_var']['rv'+str(i+1)].values[0])

    date_promo=[]
    for i in range(int(config_All_india_promo[config_All_india_promo['derived_dimension']=='date_var']['num_rav_var'].values[0])):
        date_promo.append(config_All_india_promo[config_All_india_promo['derived_dimension']=='date_var']['rv'+str(i+1)].values[0])

    #creating a Price column
    p_config=config_All_india_promo[config_All_india_promo['derived_dimension']=='Price']
    #applying for multivariables the pandas eval for finding the values of the Price and specs
    a_dict = {}
    for i in range(int(p_config['num_rav_var'].sum())):
        a_dict[p_config['rv'+str(i+1)].sum()]='rv'+str(i+1)
    a=test_data_all.rename(columns=a_dict).eval(p_config['formula'])
    test_data_all['Price']=a[0]
    
    test_data_all.drop(columns=col_drop(hier,hier_list),inplace=True)

    #SPENDS=config_All_india_promo[config_All_india_promo['derived_dimension']=='Spends']['rv'+str(1)].values[0]
    PCV=config_All_india_promo[config_All_india_promo['derived_dimension']=='PCV']['rv'+str(1)].values[0]
    SALES=config_All_india_promo[config_All_india_promo['derived_dimension']=='Sales']['rv'+str(1)].values[0]
    zone_reg_col=[] 
    for i in range(2):
            zone_reg_col.append(config_All_india_promo[config_All_india_promo['derived_dimension']=='geo_level']['rv'+str(i+1)].values[0])

    #Below is the code if config file contain the column names of the spends as different columns
    pre1.channel_list=[]
    for i in range(int((config_All_india_promo[config_All_india_promo['derived_dimension']=='promotion']['num_rav_var'].sum()))):
        pre1.channel_list.append(config_All_india_promo[config_All_india_promo['derived_dimension']=='promotion']['rv'+str(i+1)].sum())

    pre1.lr={}
    pre1.decay={}
    for i in range(config_All_india_promo[config_All_india_promo['derived_dimension']=='Learning Rates']['num_rav_var'].sum()):
        pre1.lr[pre1.channel_list[i]]=config_All_india_promo[config_All_india_promo['derived_dimension']=='Learning Rates']['rv'+str(i+1)].sum()
        pre1.decay[pre1.channel_list[i]]=config_All_india_promo[config_All_india_promo['derived_dimension']=='Decay Rates']['rv'+str(i+1)].sum()

    #treating outliers in the model removing the values over 99%
    filling_na(data_promo,hier_list[2],zone_reg_col,pre1.channel_list)

    list_d_hier=list(date_promo)+hier_list[0:3]+zone_reg_col#list containing [Month,Manufacture,Brand,Subbrand,Zone,Region]
    data_promo_2=data_promo.groupby(by=list(set(list_d_hier)-set(col_drop(hier,hier_list)))).sum().reset_index()
    data_promo1= pd.merge(test_data_all,data_promo_2, on =list(set(list_d_hier)-set(list(col_drop(hier,hier_list)))),how='left')
    data_promo1.rename(columns={SALES:'Sales',PCV:'PCV'},inplace=True)

    #columns not to drop(non promo,sales,promo(nad stock),date)
    non_promo_col=['Price','PCV']
    non_drop_col=list(date_promo)+[hier]+list(pre1.channel_list)+['Sales']+non_promo_col + zone_reg_col
   
    #replacing any nan due to division for taking log later
    mean=data_promo1['Price'].mean()
    data_promo1['Price'].fillna(mean,inplace=True)
    data_promo1.Price.replace(to_replace={0.0:mean},inplace=True)
    #a=zeroes_finder(data_promo1)
    rep_zero(data_promo1,'PCV')

    spc_hier_list = list(data_promo1[hier].unique())
     #droppping other columns 
    data_promo1.drop(columns=list(set(list(data_promo1.columns))-set(non_drop_col)),inplace=True)

    
    for i in (pre1.channel_list):
        for j in spc_hier_list: 
            ad_stock_s_curve_u(data_promo1,data_promo,i,hier,j,zone_reg_col,pre1.lr,pre1.decay)
# =============================================================================
#             log_var_crores(data_promo1,str('ad_stock_nad_')+i)
#             log_var_crores(data_promo1,str('ad_stock_s_')+i)
# =============================================================================
# =============================================================================
#     log_var(data_promo1,'Sales')
#     log_var(data_promo1,'PCV')
#     log_var(data_promo1,'Price')
# =============================================================================
    
    #CHECK FOR CORRELATION AND RELATED CHANGES 
    
    #GET THE LIST OF COLUMNS TO TAKE CORRELATION MATRIX FOR 
    chann=np.array(pre1.channel_list)   
    non_promo_col=np.array(['Price','PCV'])
    driver_col=[str("ad_stock_nad_")+i for i in chann.astype('object')]+[j for j in non_promo_col.astype('object') ]
    lis=driver_col+['Sales']
    
    #CORRELATION MATRIX 
    corr= data_promo1[lis].corr() 
     
    cor1_dict= corr_find(data_promo1,pre1.channel_list,cor_coef_ad,cor_coef_else)
    #get the mapped dictionary ex. 'Digital' : 'ad_stock_nad_Digital_log
    mapped=new_map_dict(corr_find.corr) 
    pre1.added_col1=deque([]) 
    pre1.added_col2=deque([])
    data_promo1,pre1.chann_list,pre1.added_col1,pre1.added_col2=corr_merge_zone(pre1.added_col1,pre1.added_col2,data_promo,data_promo1,hier,spc_hier,zone_reg_col,channel_list,spc_hier_list,mapped,cor1_dict,cor_coef_ad,cor_coef_else,lr,decay)
    #we get return as df, new channel_list and the list of exchanges of columns in deque
    
    #GET DUMMIES FOR SEASONALITY 
    data_promo1[date_promo[0]]=data_promo1[date_promo[0]].dt.month
    #CREATING 4 BINS 
    data_promo1[date_promo[0]]=pd.cut(data_promo1[date_promo[0]],4,labels=[str('season_')+str(i) for i in range(4)])
    #CREATING DUMMY VARIABLES 
    daa=pd.get_dummies(data_promo1[date_promo[0]])
    #JOIN BOTH
    data_promo1 = data_promo1.join(daa)
    
    return data_promo1



