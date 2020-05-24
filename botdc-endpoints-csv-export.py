# encoding = utf-8

import json
import requests
import re
import pandas

hostname =	"csp.infoblox.com"
api_token =	"" #Your csp API key here
headers= {"Authorization": "Token {}".format(api_token)}

def get_endpoints(hostname,api_token):
    offset=0
    while 1:
        response = requests.get("https://{}/api/atcep/v1/roaming_devices?_limit=10000&_offset={}".format(hostname,offset), headers=headers, verify=True, timeout=(300,300))
        try:
            r_json = response.json()
            print(r_json)

            if len(r_json["results"])==0:
                return 0
            
            df= pandas.DataFrame.from_dict(pandas.json_normalize(r_json["results"], max_level=3))
            if offset > 0:
                df.to_csv('export.csv', mode='a',header=False)
            else:
	            df.to_csv('export.csv', header=True)
            offset+=10000
        except:
        	raise Exception
        	break
    
get_endpoints(hostname,api_token)
