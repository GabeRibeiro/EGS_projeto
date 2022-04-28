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
from make_requests import influx



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
    
def send_influx():
    pass

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

def create_entry(measurement, tags, timestamp, fields):
    """
    creates a json like influx db entry
    """
    return [{"measurement": measurement, "tags" : tags, "time" : timestamp, "fields": fields}]


#clientCount by location ... tem que estar tudo no mesmo field
def merge_entrys2(entrys,data):
    for row in [row for row in data]:
        for entry in entrys:
            for key in [key for key in entry if not key in row]:
                row[key] = entry[key]
            for key in [key for key in row if not key in entry]:
                entry[key] = row[key]
            data.append(entry)
    print('finaly')
    return data
"""
def merge_entrys(entrys,data):
    merge_result = [] 
    merge_data = {}

    for row in entrys:
        merge_row = {}
        if row.keys() != data[0].keys():
            for key in row:
                if not key in data[0].keys():
                    merge_data[key] = row[key]
                else:
                    merge_row[key] = data[0][key]
        for key in merge_row:
            row[key] = merge_row[key]
        print(row)
        data.append(row)

    for val in data:
        for key in merge_data:
            val[key] = merge_data[key]

            
    for val in [val for val in data]:
        aux = val
        for row in entrys:
            #entrys.remove(row)
            #data.remove(val)
            if row.keys() != val.keys():
                
                #print('aux',aux)
                #print('val',val)
                for key in row:
                    if not key in val:
                        #print(val,key)
                        val[key] = row[key]
                #val.update(row)
                for key in val:
                    if not key in row:
                        row[key] = val[key]
            #if row.keys() == val.keys():
            #data.append(row)    
            #data.append(aux)
            data.append(row)
        data.append(aux)
        break
                
            #merge_result.append(row)
         


    #for row in entrys:
    #    print('ASDASDASD')
    #    data.append(row)

    return data
    

def merge_entrys3(entrys,data):
    for val in data:
        print('mmmmmmmmmmh')
        for entry in entrys:
            for key in val:
                if not key in entry:
                    entry[key] = val[key]
            for key in entry:
                if not key in val:
                    val[key] = entry[key]
    
            data.append(entry)

    return data 
"""
"""
def merge_entrys(entrys,data):
    merge_result = [] 
    for val in [val for val in data]:

        for row in [row for row in entrys if row.keys() == val.keys()]:
            merge_result.append(row)
            entrys.remove(row)

        for row in entrys:
            row.update(val)
            merge_result.append(row)
            entrys.remove(row)

    return merge_result
"""
"""
# não é utilizado
def merge_all(entrys,data):
    # vai adicionar o elemento de uma lista com as mesmas keys
    for row in [row for row in entrys if row.keys() == data[0].keys()]:
        data.append(row)
        entrys.remove(row)
        
    # vai ver as keys que não estão na data    
    # como supostamente as keys na data são iguais para todos os membros só é preciso ver o primeiro
    merge_data = {}
    for key in [key for key in data[0] if not key in entrys[0]]:
        merge_data[key] = data[0][key]
    
    # adicionar as keys ás novas entradas
    for entry in entrys:
        entry.update(merge_data)
        data.append(entry)
        
    # é preciso limpar os elementos de data ... 
    # caso as keys sejam diferentes pode adicionar as keys de data a entrys 
    # mas algumas entradas de data ficam sem as keys de entrys
    # é preciso remover esses casos ...
    if entrys:
        for entry in data:
            if len(entry.keys()) < len(entrys[0].keys()):
                data.remove(entry)
        
    return data

def merge_fields(field,data):
    for row in field:
        for val in data:
            val.update(row)
    return data
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


# gramatica ... clientCount, location and macAddress
# 
"""
args = ["clientCount","location","macAddress"]
url = 'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult='
#url = 'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/RogueAccessPointAlarm?maxResult=1000&firstResult='
#url = 'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/RogueAccessPointAlarm?id='
#url = 'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/Building'
token_url = 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid'
secret = 'BrszH8oF9QsHRjiOAC1D9Ze0Iloa'
auth_type = 'Bearer'
content_type = 'application/x-www-form-urlencoded'
key = 'j_mGndxK2WLKEUKbGrkX7n1uxAEa'
# get_token(url,key,secret,content_type=None,auth_type=None)
token = get_token(token_url,key,secret,content_type,auth_type)
for i in range(8):
    r = make_request_token(url+(str(i*10)),token)
    print(r)
    print(r.json())
    send_influx(r.json(),args)
"""
