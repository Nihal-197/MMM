from flask import make_response, jsonify

import pandas as pd
import numpy as np
import os
import re


def check_input(data, requried_fields=[]):
	"""
		required_fields: These are the field that are required for the api to get output.
	"""
	keys = data.keys()
	if not all([field in keys for field in requried_fields ]):
		raise ValueError("FIELDS MISSING")
	
def json_response(data='', status=204, headers=None):
	return make_response(jsonify(data), status, {'Content-Type': 'application/json'})

def non_neg_val(data_json,channel_list):
    req_fields= [i for i in channel_list]+['PCV','Price']
    if not all(data_json[keys]>=0 for keys in req_fields):
        raise ValueError('All the values must be non-negative')
    #PCV should be between 0 to 100
    if not( data_json['PCV']>=0 and data_json['PCV']<=100):
        raise ValueError('PCV should be between 0 to 100')

def has_string(string):
    return bool(re.search('[a-zA-Z]',string))

def has_number(string):
    return bool(re.search('[0-9]',string))

def is_a_number(num):
    return bool(type(num)==float or type(num)==int)

#implement the input value part 2
def input_val_part2(data_json,fields):
    print([is_a_number(data_json[i])  for i in fields])
    if not all([is_a_number(data_json[i])  for i in fields]):
        raise ValueError('enter digits only')


def data_validator(data_promo,zone,zone_name):
    zone_list= list(data_promo[zone].unique())
    for i in range(len(zone_list)):
        if zone_name==zone_list[i]: 
            print('{} validated'.format(zone_name))
            break
        if i==(len(zone_list)-1):
           raise ValueError('please give valid details')
      
def val_hier(config_ALL_india_promo,hier):
    dat=config_All_india_promo[config_All_india_promo['derived_dimension']=='target_dim']
    for i in range(dat['num_rav_var'].sum()):
        if (hier==dat['rv'+str(i+1)][0]):
            break
        if (i==(dat['num_rav_var'].sum()-1)):
            raise ValueError('The given input does not match in hierarchy')

def hier_val(config_All_india_promo,hier):
    dat=config_All_india_promo[config_All_india_promo['derived_dimension']=='target_dim']
    for i in range(dat['num_rav_var'].sum()):
        if (hier==dat['rv'+str(i+1)][0]):
            break
        if (i==2):
            raise ValueError('please give valid details')