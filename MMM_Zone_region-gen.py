#==============================================================================
#IMPORTING LIBRARIES
import pandas as pd
import numpy as np
import json 
from flask import Flask, request, jsonify
from utils import *
import warnings
warnings.filterwarnings('ignore')
from api_test1 import *
from eql_testing import *
#==============================================================================

#==============================================================================
#LOADING THE DATA
config_All_india_promo=pd.read_csv(r'C:\Users\Nihal\Downloads\config_All_india_promo2.csv')
config_All_india_HFD=pd.read_csv(r'C:\Users\Nihal\Downloads\config_All_india_HFD.csv')
#create an EQL function for fetching the data using the inputs 

# =============================================================================
# eql_generator_mmm_HFD(data_dict_1,config_All_india_promo,"activity","find","transaction")
# eql_generator_mmm_spends(data_dict_2,config_All_india_promo,"activity","find","transaction")
# 
# =============================================================================
#fetch the data with that EQL function


data_promo = pd.read_csv(r'C:\Users\Nihal\Downloads\Data_prep_v8.csv',engine='python')
data_HFD = pd.read_csv(r'C:\Users\Nihal\Downloads\HFD_output_v11_v9.csv',engine='python')
#==============================================================================

#==============================================================================
#FILTERING DATA 
data_HFD['month']=pd.to_datetime(data_HFD['month'],format='%Y-%m-%d')
data_promo['Month']=pd.to_datetime(data_promo['Month'],format='%m/%d/%Y',errors='ignore')
data_HFD.rename(columns={'month':"Month",'Urbanrural':'Region'},inplace=True)
data_promo = data_promo.pivot_table(r'Spend(In Crore)', ['Month', 'Manufacturer','Brand','Subbrand',
                                           'Zone','Region' ], 'Channel')
data_promo.reset_index(inplace=True)
data_HFD.Subbrand.replace(to_replace={'BOOST HEALTH AND ENERGY\xa0':'BOOST HEALTH AND ENERGY'},inplace=True)
data_promo.Subbrand.replace(to_replace={'BOOST HEALTH AND ENERGYÂ\xa0':'BOOST HEALTH AND ENERGY'},inplace=True)
# =============================================================================

""" 
	Python MMM API
	@API Version: 2.0.0
	@Author: Nihal 
	@Date: 28.06.2019
"""

app = Flask(__name__)

@app.before_request
def check_request():
	try:
		# Validate api_key and api_secret here

		if not request.data:
			raise ValueError("Request needs a data")
		if request.content_type != 'application/json':
			raise ValueError("Input should be of type application/json")
		
		input_json = request.data.decode("utf-8")
		check_input(json.loads(input_json), requried_fields=['api_key','api_secret'])
		print("all checks done")
	except ValueError as e:
		return json_response({"status_code":"400", 'status_txt':'BAD REQUEST ' + str(e)},status=400)
	except Exception as e:
		return json_response({"status_code":"400", "status_txt":'BAD REQUEST ' + str(e.__class__.__name__)}, status=400)

#TO GET THE DATA FROM THE EQL 
def get_data(eql_generated, api_key=None, api_secret=None, limit=None):
    """ Get the needed data from the API """
 
    data_payload = {
    'api_key': api_key,
    'api_secret': api_secret, 
    'data': {eql: eql_generated}
        }
 
    data_header = { 
    'content-type': 'application/json'
    }
    response = requests.request("POST", url=config.EQL_PROCESSOR_URL, json=data_payload, headers=data_header)
    data = response.json()
     
    if data['status_code'] != 200:
        raise ValueError(data["status_txt"])
    if not data['data']:
        raise ValueError(data["status_txt"])
    if 'status_code' in data['data']:
        raise ValueError(data['data']["status_txt"])
         
    return data


@app.after_request
def check_response(response):
	return response


{ 
    
        "api_key":456,
        "api_secret": 456,
        "hier": "Brand",
        "spc_hier": "COMPLAN",
        "mod": "Zone", 
        "zone": "SOUTH",
        "region": "RURAL"
        
    }

{ 
    
    "Digital": 0.036340515999999996*1.1,
    "OOH": 0.004845402*1.1,
    "Print": 0.063268643*1.1,
    "Radio":0.002422701*1.1, 
    "TV":0.15747557*1.1,
    "PCV": 19.405712061209467, 
    "Price": 0.7841174974565274,
    "Budget" : 5
        
    }

@app.route('/mixed_models/', methods=['POST'])
def mmm_api():
    if request.method=='POST':
        print('MMM_model')
        data_json_sample = request.data.decode("utf-8")
        data_json_sample=json.loads(data_json_sample)   
    try:
        data = MMM1(data_HFD,data_promo,config_All_india_HFD,config_All_india_promo,data_json_sample)
        return json_response({"status_code":"200","data":data, 'status_txt':'SUCCESS'},status=200)
    except ValueError as e:
        return json_response({"status_code":"500", 'status_txt':' INTERNAL SERVER ERROR, '+str(e).upper()},status=500)
    except Exception as e:
        return json_response({"status_code":"500", 'status_txt':' INTERNAL SERVER ERROR! '+str(e)},status=500)
@app.route('/mixed_models/promotional_input/', methods=['POST'])
def mmm_api2(): 
    data_json_1 = request.data.decode("utf-8")
    data_json2=json.loads(data_json_1)
    try: 
        data_final = final(MMM1.data_promo1,MMM1.hier,MMM1.spc_hier,MMM1.added_col1,MMM1.added_col2,MMM1.channel_list,MMM1.chann_list,MMM1.driver1_sea,MMM1.driver1,MMM1.mdf1_sea,MMM1.lr,MMM1.decay,config_All_india_promo,data_json2,MMM1.mod)
        return json_response({"status_code":"200","data":data_final, 'status_txt':'SUCCESS'},status=200)
        #return jsonify(data_final)

    except ValueError as e:
        return json_response({"status_code":"500", 'status_txt':' INTERNAL SERVER ERROR, '+str(e).upper()},status=500)
    except Exception as e:
        return json_response({"status_code":"500", 'status_txt':' INTERNAL SERVER ERROR! '+str(e)},status=500)


if __name__ == '__main__':
	app.run(debug = True)
