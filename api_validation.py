import pandas as pd 
import re
def has_string(string):
    return bool(re.search('[a-zA-Z]',string))
def has_number(string):
    return bool(re.search('[0-9]',string))
        
def data_validator(data_promo,zone,zone_name):
    zone_list= list(data_promo[zone].unique())
    for i in range(len(zone_list)):
        if zone_name==zone_list[i]:
            break
        if i==(len(spc_hier_list)-1):
           return print('Incorrect name: {}'.format(zone_name))
def val_hier(config_ALL_india_promo,hier):
    dat=config_All_india_promo[config_All_india_promo['derived_dimension']=='target_dim']
    for i in range(dat['num_rav_var'].sum()):
        if (hier==dat['rv'+str(i+1)][0]):
            break
        if (i==(dat['num_rav_var'].sum()-1)):
            return print('Incorrect Name {}'.format(hier))

def hier_val(config_All_india_promo,hier):
    dat=config_All_india_promo[config_All_india_promo['derived_dimension']=='target_dim']
    for i in range(dat['num_rav_var'].sum()):
    if (hier==dat['rv'+str(i+1)][0]):
        break
    if (i==2):
        return print('match not found for {}'.format(hier))