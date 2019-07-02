import pandas as pd
import numpy as np
from mmm_model import *
from mmm_post_pro import *
from mmm_pre_zone import * 
from mmm_pre_all import *
from corr_finder import *
from post_procs_part2 import *
import json 
from flask import Flask, request, jsonify
from utils import *
import warnings
warnings.filterwarnings('ignore')

#==============================================================================
#MMM
def MMM1(data_HFD,data_promo,config_All_india_HFD,config_All_india_promo,data_json):
    
    #==========================================================================
    #Raising error in the data provided itself
    #then checking for the columns in the pre_processing module
    
    if not has_string(data_json['hier']):
        raise ValueError('Please write the Hierarchy name correctly')
    
    if has_number(data_json['hier']):
        raise ValueError('Please write the Hierarchy name correctly, must not contain any number')
    
    
    MMM1.hier=data_json['hier'].capitalize()#manufacute/Brand/Subbrand
    hier_val(config_All_india_promo,MMM1.hier)
    print('{} Validated'.format(data_json['hier']))
   
    if not has_string(data_json['spc_hier']):
        raise ValueError('Please write the name correctly')
    
    if has_number(data_json['spc_hier']):
        raise ValueError('Please write the name correctly, must not contain any number')
    
    MMM1.spc_hier=data_json['spc_hier'].upper()
    data_validator(data_promo,MMM1.hier,MMM1.spc_hier)
    
    if not has_string(data_json['mod']):
        raise ValueError('Please define the geo level correctly')
    
    if has_number(data_json['mod']):
        raise ValueError('Please write the geo level correctly, must not contain any number')
    print('mod done')

    #CHOOSING HIER,etc.
    
    #specific_hier galaxo/horlicks/horlickslite
   
    #ALLINDIA MODEL/ ZONE_REGION MODEL
    MMM1.mod=data_json['mod'].capitalize()
    
    if MMM1.mod=='Zone':
        if not has_string(data_json['zone']):
            raise ValueError('Please write the zone correctly')
        if not has_string(data_json['region']):
            raise ValueError('Please write the region correctly')
        MMM1.zone =data_json['zone'].capitalize()
        MMM1.region=data_json['region'].capitalize()
        
        data_validator(data_promo,'Zone',MMM1.zone)
        data_validator(data_promo,'Region',MMM1.region)
        
        #==========================================================================
        #FILTER FOR ZONAL DATA 
        test_data_all=data_HFD[(data_HFD['Level']==MMM1.hier)&(data_HFD['Level_Geo']=='Zone')]
        test_data_all=test_data_all[(test_data_all['Zone']==MMM1.zone)&(test_data_all['Region']==MMM1.region)].reset_index(drop=True)
        
# =============================================================================
#         #This filter is already provided with EQL
#         test_data_all=test_data_all[['Zone', 'Region','Month', 'Sales Volume (Volume(LITRES))','WD PCV Handling%','Value Offtake(000 Rs)']+[MMM1.hier]]
#         data_promo=data_promo[['Zone', 'Region','Month']+[MMM1.hier]+channel_list]
#         
# =============================================================================
        #==========================================================================
    
        #=========================PREPROCESSING====================================
        MMM1.data_promo1=pre1(test_data_all,data_promo,config_All_india_HFD,config_All_india_promo,MMM1.hier,MMM1.spc_hier,0.89,0.8)
        print('Pre processing done for Zone')
        
        #=============================MODEL============================================
        Model(MMM1.data_promo1,MMM1.hier,pre1.chann_list)
        print('Model trained')
        print(f'R-2 score :{Model.acc1}')
        print(f'R-2 score with seasons : {Model.acc2}')
        
        #========================USER_INPUT============================================
        final_data1=user_input(MMM1.data_promo1,MMM1.hier,MMM1.spc_hier,pre1.channel_list,Model.mdf1_sea,Model.mdf1,pre1.lr,pre1.decay,config_All_india_promo,data_json,pre1.chann_list,pre1.added_col1,pre1.added_col2)
        MMM1.channel_list= pre1.channel_list.copy()
        MMM1.lr= pre1.lr.copy()
        MMM1.decay = pre1.decay.copy() 
        MMM1.mdf1= Model.mdf1
        MMM1.mdf1_sea= Model.mdf1_sea
        MMM1.driver1=Model.driver1
        MMM1.driver1_sea=Model.driver1_sea
        MMM1.chann_list = pre1.chann_list
        MMM1.added_col1 = pre1.added_col1
        MMM1.added_col2 = pre1.added_col2

        return final_data1
    #==============================================================================
    if(MMM1.mod=='Allindia' or MMM1.mod=='allindia' or MMM1.mod=='All india' or MMM1.mod=='AllIndia' or MMM1.mod=='all india'):
        
        #==========================================================================
        #FILTERING ALL INDIA DATA 
        test_data_all=data_HFD[(data_HFD['Level']==MMM1.hier)&(data_HFD['Level_Geo']=='Country')] #changes made(changed from country == all india)
        #==========================================================================
  
    # =============================================================================
#         #This filter is already provided with EQL            
#         test_data_all=test_data_all[['Month', 'Sales Volume (Volume(LITRES))','WD PCV Handling%','Value Offtake(000 Rs)']+[MMM1.hier]]
#         data_promo=data_promo[['Month']+[MMM1.hier]+channel_list]
#         
# =============================================================================

        #=========================PREPROCESSING====================================
        MMM1.data_promo1=pre2(test_data_all,data_promo,config_All_india_HFD,config_All_india_promo,MMM1.hier,MMM1.spc_hier,0.99,0.9)
        #==========================================================================
        print('Pre processing done for AllIndia')
        
        #=============================MODEL============================================
        Model(MMM1.data_promo1,MMM1.hier,pre2.chann_list)
        print('Model trained')
        print(Model.driver1_sea)
        #========================USER_INPUT============================================
        final_data1=user_input(MMM1.data_promo1,MMM1.hier,MMM1.spc_hier,pre2.channel_list,Model.mdf1_sea,pre2.lr,pre2.decay,config_All_india_promo,data_json,pre2.chann_list,pre2.added_col1,pre2.added_col2)

        MMM1.channel_list= pre2.channel_list.copy()
        MMM1.lr= pre2.lr.copy()
        MMM1.decay = pre2.decay.copy()
        MMM1.mdf1= Model.mdf1
        MMM1.mdf1_sea= Model.mdf1_sea
        MMM1.driver1=Model.driver1
        MMM1.driver1_sea=Model.driver1_sea
        MMM1.chann_list = pre2.chann_list
        MMM1.added_col1 = pre2.added_col1
        MMM1.added_col2 = pre2.added_col2
        return final_data1
        #Saving few variables 
    #==============================================================================
    #create a post_processing part 2 for taking next few inputs
def final(data_promo1,hier,spc_hier,added_col1,added_col2,channel_list,chann_list,driver1_sea,driver1,mdf1_sea,lr,decay,config_All_india_promo,data_json,mod):
    
    #function just for checking if it contains the values 
    check_input(data_json,['api_key','api_secret']+[i for i in channel_list]+['PCV','Price'])
    
    #check if the PCV has value between  0-100 as its a percentage and the rest of the values cannot be negative
    non_neg_val(data_json,channel_list) 

    final_data2=user_input_part2(data_promo1,hier,spc_hier,added_col1,added_col2,channel_list,chann_list,driver1_sea,driver1,mdf1_sea,lr,decay,config_All_india_promo,data_json,mod)
    return final_data2
    
