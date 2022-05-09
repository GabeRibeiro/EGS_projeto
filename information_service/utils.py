# ficheiro com utils como make request
# get token
# make request_key
# make request_open
import requests
import json
import base64
import pytz
from pytz import timezone, common_timezones
from datetime import datetime


def make_request(url):  
    r = requests.get(url,timeout=15)
    if r.status_code == 200:
        return r.json()
    return display_error(r.status_code)
        

def make_request_key(url,key):
    return requests.get(url,headers={'Authorization': key},timeout=15)
   
def make_request_http(url,user,key):
    return requests.get(url,headers={"userName": user , "password": key},timeout=15)

def make_request_token(url,token):
    return requests.get(url,headers={'Authorization': token},timeout=15)
    

# para o wso2 content_type -> application/x-www-form-urlencoded | auth_type -> Bearer
def get_token(url,key,secret,content_type=None,auth_type=None):
    msg = encode_b64(key+':'+secret)
    #print(msg=='al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h')
    request_token = requests.post(url,headers={'Content-Type': content_type, 'Authorization': 'Basic '+msg},timeout=15)
    if request_token.status_code < 400:
        return auth_type + ' ' + request_token.json()['access_token'] if auth_type else request_token.json()
    return display_error(request_token.status_code)

def display_error(request_status):
    if request_status == 404:
        return "URL Not Found"
    elif request_status == 401:
        return "Authentication Error"
    elif request_status == 403:
        return "URL FORBIDEN OPERATION"
    return "Bad Request"

def encode_b64(msg):
    msg_bytes = msg.encode('ascii')
    base64_bytes = base64.b64encode(msg_bytes)
    return base64_bytes.decode('ascii')

def get_timestamp():
    portugal_tz = timezone("Europe/Lisbon")
    return portugal_tz.localize(datetime.now())

def epoch2utc(timestamp):
    return datetime.fromtimestamp(timestamp, pytz.utc)

#def create_entry(measurement, tags, timestamp, fields):
#    """
#    creates a json like influx db entry
#    """
#    return [{"measurement": measurement, "tags" : tags, "time" : timestamp, "fields": fields}]

def filter_entrys(data,tag,value):
    entrys = []
    for field in data:
        if isinstance(field,str):
            if isinstance(data[field],dict):
                entrys += filter_entrys(data[field],tag,value)
            elif isinstance(data[field],list):
                entrys += filter_entrys(data[field],tag,value)
            elif field == tag or field == value:
                entrys += [(data[tag],data[value])]
                break
        elif isinstance(field,dict):
            entrys += filter_entrys(field,tag,value)
        elif isinstance(field,list):
            entrys += filter_entrys(field,tag,value)
        
    return entrys

"""
def merge_entrys(entrys,fields):
    for entry in entrys:
        entry.update(fields)
    return entrys 

def merge_fields(field,data):
    for row in field:
        for val in data:
            val.update(row)
    return data
    
def merge_entrys(entrys,fields):
    for entry in entrys:
        entry.update(fields)
    return entrys 

def merge_filter(data,args):
    entrys = []
    fields = {}
    for field in [field for field in data]:
        if isinstance(field,str):       
            if isinstance(data[field],dict):
                aux = merge_filter(data[field],args)
                if len(aux) == 1:
                    fields.update(aux[0])
                elif aux:
                    entrys += aux
            elif not isinstance(data[field],str) and isinstance(data[field],list): 
                aux = []
                for val in data[field]:
                    aux += merge_filter(val,args)
                entrys += merge_entrys(aux,fields)
                
            elif args == 1:
                fields[field] = data[field]
            elif field in args:
                fields[field] = data[field]                    
        
        elif isinstance(field,dict):
            entrys += merge_filter(field,args)
        
        elif isinstance(field,list):
            aux = []
            for val in field:
                aux += merge_filter(val,args)
            entrys += aux
               
    return merge_entrys(entrys,fields)  if entrys else [fields]
"""