from utils import *
from make_requests import Query
from datetime import datetime as dt

tokens = {}

def request_basic(metric_id,url,value,tag):
    try:
        request = requests.get(url,timeout=40)
    except:
        print('Connection error')
        return
    if request.status_code < 400: 
        try:
            db_entrys = filter_entrys(request.json(),tag,value)
            if db_entrys:
                try:
                    for entry in [entry for entry in db_entrys if entry]:
                        Query.add_value(metric_id,entry[0],entry[1])
                except:
                    print('writing values failed')
            else:
                Query.pause_url(metric_id)
                print('BAD FORMAT BASIC')
        except:
            Query.pause_url(metric_id)
            print("FILTER FAILED")         
    elif request.status_code == 401:
        Query.pause_url(metric_id)
        print('Authentication Error')
    elif request.status_code == 403:
        Query.pause_url(metric_id)
        print("URL FORBIDEN OPERATION")
    elif request.status_code == 404:
        Query.pause_url(metric_id)
        print('URL NOT FOUND')
    elif request.status_code < 500:
        Query.pause_url(metric_id)
        print('bad request')
    else:
        print('Internal Server Error')
    return False

def request_key(metric_id,url,value,tag,key,name):           
    try:
        request = requests.get(url,headers={name: key},timeout=40)
    except:
        print('Connection error')
        return
    if request.status_code < 400:
            try:
                db_entrys = filter_entrys(request.json(),tag,value)
                if db_entrys:
                    try:
                        for entry in db_entrys:
                            Query.add_value(metric_id,entry[0],entry[1])
                    except:
                        print('writing values failed')
                else:
                    print('BAD FORMAT')
                    Query.pause_url(metric_id)
            except:
                Query.pause_url(metric_id)
                print("FILTER FAILED")
            
    elif request.status_code == 401:
        Query.pause_url(metric_id)
        print('Authentication Error')
    elif request.status_code == 403:
        Query.pause_url(metric_id)
        print("URL FORBIDEN OPERATION")
    elif request.status_code == 404:
        Query.pause_url(metric_id)
        print('URL NOT FOUND')
    elif request.status_code < 500:
        print('bad request')
        Query.pause_url(metric_id)
    else:
        print('Internal Server Error')
        
    return False

def request_http(metric_id,url,value,tag,username,key):      
    try:
        request = requests.get(url,headers={"username": username , "password": key},timeout=40)
    except:
        print('Connection error')
        return
    if request.status_code < 400:    
        try:
            db_entrys = filter_entrys(request.json(),tag,value)
            if db_entrys:
                try:
                    for entry in db_entrys:
                        Query.add_value(metric_id,entry[0],entry[1])
                except:
                    print('writing values failed')
            else:
                print('BAD FORMAT')
                Query.pause_url(metric_id)
        except:
            Query.pause_url(metric_id)
            print("FILTER FAILED")       
    
    elif request.status_code == 401:
        Query.pause_url(metric_id)
        print('Authentication Error')
    elif request.status_code == 403:
        Query.pause_url(metric_id)
        print("URL FORBIDEN OPERATION")
    elif request.status_code == 404:
        Query.pause_url(metric_id)
        print('URL NOT FOUND')
    elif request.status_code < 500:
        print('bad request')
        Query.pause_url(metric_id)
    else:
        print('Internal Server Error')
        
    return False
        
def request_token(metric_id,url,value,tag,token_url,key,secret,content_type,auth_type,period):
    msg = encode_b64(key+':'+secret)
    
    if metric_id in tokens:
        token = tokens[metric_id]
    else:
        try:
            request = requests.post(token_url,headers={'Content-Type': content_type, 'Authorization': 'Basic '+msg},timeout=15)
        except:
            print('Connection error')
            return
        if request.status_code<300:
            token = auth_type + ' ' + request.json()['access_token']
            tokens[metric_id] = token
        elif request.status_code == 401:
            Query.pause_url(metric_id)
            print('Token Authentication Error')
            return 
        elif request.status_code == 403:
            Query.pause_url(metric_id)
            print("Token URL FORBIDEN OPERATION")
            return
        elif request.status_code == 404:
            Query.pause_url(metric_id)
            print('Token URL NOT FOUND')
            return
        elif request.status_code < 500:
            print('Token Bad Request')
            Query.pause_url(metric_id)
            return
        else:
            print('Token Internal Server Error')
            return
        if period<60:
            tokens[metric_id] = token
        
    try:
        request = requests.get(url,headers={'Authorization': token},timeout=40)
    except:
        print('Connection error')
        return
    if request.status_code == 401 and period<60:
        try:
            request = requests.post(token_url,headers={'Content-Type': content_type, 'Authorization': 'Basic '+msg},timeout=15)
        except:
            print('Connection error')
            return
        token = auth_type + ' ' + request.json()['access_token']
        tokens[metric_id] = token
        try:
            request = requests.get(url,headers={'Authorization': token},timeout=40)
        except:
            print('Connection error')
            return
    if request.status_code < 400:
        try:
            db_entrys = filter_entrys(request.json(),tag,value)
            if db_entrys:
                try:
                    for entry in db_entrys:
                        Query.add_value(metric_id,entry[0],entry[1])
                except:
                    print('writing values failed')
            else:
                print('BAD FORMAT')
                Query.pause_url(metric_id)
        except:
            Query.pause_url(metric_id)
            print("FILTER FAILED") 
    elif request.status_code == 401:
        Query.pause_url(metric_id)
        print('Authentication Error')
    elif request.status_code == 403:
        Query.pause_url(metric_id)
        print("URL FORBIDEN OPERATION")
    elif request.status_code == 404:
        Query.pause_url(metric_id)
        print('URL NOT FOUND')
    elif request.status_code < 500:
        print('bad request')
        Query.pause_url(metric_id)
    else:
        print('Internal Server Error')
        
    return False
