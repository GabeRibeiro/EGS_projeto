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