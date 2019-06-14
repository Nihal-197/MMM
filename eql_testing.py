import pandas as pd
import json

#CONFIG FILE IN A DATAFRAME

def get_line(config,derived_name):
    return config[config['derived_dimension']==derived_name] #can make a function returning a list with rv1 values

def eql_generator_mmm_HFD(data_json,config,db_type,query_type,type_):#dataframe config
    eql={}
    eql["date"]={get_line(config,"date_var")['rv1'].values[0]:{}}
    eql["db_type"]=db_type
    eql["query_type"]=query_type
    eql["type"]=type_
    eql["filter"]={"and":
                   {"eq":
                    {"Level_Geo":[
                                data_dict["mod"] 
                                        ],
                    
                    "Level":[
                                data_dict["hier"]
                                ]
                    }
                }
            }
   
        
    eql["measure"]={
    get_line(config,"Sales")['rv1'].values[0]:{},
    get_line(config,"PCV")['rv1'].values[0]:{},
    get_line(config,"Price")['rv1'].values[0]:{}, #assuming rv1 is not same as sales
                        }
    eql["dimension"]={}
    eql["db_name"]="HFD_output_v11_v9_activity"
    #appending hier values in dict
    eql["dimension"][data_dict["hier"]]={}
    #appending zone,region in dict
    if (data_dict["mod"]=="Zone"):
        tar_dim=get_line(config,"geo_level")
        for i in range(tar_dim['num_rav_var'].values[0]):
            eql["dimension"][tar_dim['rv'+str(i+1)].values[0]]={}
    return json.dumps(eql)


def eql_generator_mmm_spends(data_json,config,db_type,query_type,type_):#dataframe config
    eql={}
    eql["date"]={get_line(config,"date_var")['rv1'].values[0]:{}}
    eql["db_type"]=db_type
    eql["query_type"]=query_type
    eql["type"]=type_
        #if condition for zone and region
    eql["measure"]={}
    tar_dim=get_line(config,"promotion")
    for i in range(tar_dim['num_rav_var'].values[0]):
        eql["measure"][tar_dim['rv'+str(i+1)].values[0]]={}
    eql["dimension"]={}
    eql["db_name"]="HFD_output_v11_v9_activity"
    #appending hier values in dict
    eql["dimension"][data_dict["hier"]]={}
#     eql["dimension"][get_line(config,"Spends")['rv1'].values[0]]={}
    #appending zone,region in dict
    if (data_dict["mod"]=="Zone"):
        tar_dim=get_line(config,"geo_level")
        for i in range(tar_dim['num_rav_var'].values[0]):
            eql["dimension"][tar_dim['rv'+str(i+1)].values[0]]={}
    return json.dumps(eql)

#eql_generator_mmm(data_dict,config,"activity","find","transaction")
    
