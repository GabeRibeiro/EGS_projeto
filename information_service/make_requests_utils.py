from api_methods import Query
from utils import *
from make_requests import *
from datetime import datetime as dt

tokens = {}

def request_basic(val):
    print('STARTING BASIC\n')
    request = requests.get(val.url,timeout=40)
    if request.status_code == 200: 
        #try:
        if True:
            db_entrys = filter_entrys(request.json(),val.tag,val.value)
            if db_entrys:
                #try:
                print('entrys')
                print(request.json())
                print('\n\n')
                print(db_entrys)
                print('\n')
                for entry in [entry for entry in db_entrys if entry]:
                    print(entry)
                    
                    Query.add_values(val.metric_id,entry[0],entry[1])
                #except:
                #    print('writing values failed')
            else:
                Query.pause_basic(val[1])
                print('BAD FORMAT BASIC')
        #except:
        #    Query.pause_basic(val[1])
        #    print("FILTER FAILED")         
    
    elif request.status_code == 401:
        for val in Query.get_basic_args(url):
            Query.pause_basic(val[1])
            print('Authentication Error')
    elif request.status_code == 403:
        for val in Query.get_basic_args(url):
            Query.pause_basic(val[1])
            print("URL FORBIDEN OPERATION")
    elif request.status_code == 404:
        for val in Query.get_basic_args(url):
            Query.pause_basic(val[1])
            print('URL NOT FOUND')
    elif request.status_code < 500:
        for val in Query.get_basic_args(url):
            Query.pause_basic(val[1])
            print('bad request')
    else:
        print('Internal Server Error')
        
    return False

def request_key(val,key):       
    print('STARTING KEY\n')
    
    request = requests.get(val.url,headers={'Authorization': key},timeout=40)
    if request.status_code < 400:
            args = [arg.strip() for arg in val.args.split(',')] if val.args else 1
            print(val.url,args)
            try:
                db_entrys = filter_entrys(request.json(),val.tag,val.value)
                if db_entrys:
                    try:
                        for entry in db_entrys:
                            print(entry)
                            Query.add_values(val.metric_id,entry[0],entry[1],datetime.datetime())
                    except:
                        print('writing values failed')
                else:
                    print('BAD FORMAT')
                    Query.pause_key(val.metric_id)
            except:
                Query.pause_key(val.metric_id)
                print("FILTER FAILED")
            
    elif request.status_code == 401:
        Query.pause_key(val.metric_id)
        print('Authentication Error')
    elif request.status_code == 403:
        Query.pause_key(val.metric_id)
        print("URL FORBIDEN OPERATION")
    elif request.status_code == 404:
        Query.pause_key(val.metric_id)
        print('URL NOT FOUND')
    elif request.status_code < 500:
        print('bad request')
        Query.pause_token(val.metric_id)
    else:
        print('Internal Server Error')
        
    return False

def request_http(val,username,key):  
    print('STARTING HTTP\n')
    
    request = requests.get(val.url,headers={"username": username , "password": key},timeout=40)
    if request.status_code < 400:    
        try:
            db_entrys = filter_entrys(request.json(),val.tag,val.value)

            if db_entrys:
                try:
                    for entry in db_entrys:
                        Query.add_values(val.metric_id,entry[0],entry[1],datetime.datetime())
                except:
                    print('writing values failed')
            else:
                print('BAD FORMAT')
                Query.pause_http(val.metric_id)
        except:
            Query.pause_http(val.metric_id)
            print("FILTER FAILED")       
    
    elif request.status_code == 401:
        Query.pause_http(val.metric_id)
        print('Authentication Error')
    elif request.status_code == 403:
        Query.pause_http(val.metric_id)
        print("URL FORBIDEN OPERATION")
    elif request.status_code == 404:
        Query.pause_http(val.metric_id)
        print('URL NOT FOUND')
    elif request.status_code < 500:
        print('bad request')
        Query.pause_http(val.metric_id)
    else:
        print('Internal Server Error')
        
    return False
        
def request_token(val,token_url,key,secret,content_type,auth_type):
    print('STARTING TOKEN\n')
    msg = encode_b64(key+':'+secret)
    
    if val.metric_id in tokens:
        token = tokens[val.metric_id]
    else:
        request = requests.post(token_url,headers={'Content-Type': content_type, 'Authorization': 'Basic '+msg},timeout=15)
        if request.status_code<300:
            token = auth_type + ' ' + request.json()['access_token']
            tokens[val.metric_id] = token
        elif request.status_code == 401:
            Query.pause_token(val.metric_id)
            print('Token Authentication Error')
            return 
        elif request.status_code == 403:
            Query.pause_token(val.metric_id)
            print("Token URL FORBIDEN OPERATION")
            return
        elif request.status_code == 404:
            Query.pause_token(val.metric_id)
            print('Token URL NOT FOUND')
            return
        elif request.status_code < 500:
            print('Token Bad Request')
            Query.pause_token(val.metric_id)
            return
        else:
            print('Token Internal Server Error')
            return
        if val.period<60:
            tokens[val.metric_id] = token
        
    request = requests.get(val.url,headers={'Authorization': token},timeout=40)
    if request.status_code == 401 and val.period<60:
        request = requests.post(token_url,headers={'Content-Type': content_type, 'Authorization': 'Basic '+msg},timeout=15)
        token = auth_type + ' ' + request.json()['access_token']
        tokens[val.metric_id] = token
        request = requests.get(val.url,headers={'Authorization': token},timeout=40)
    
    if request.status_code<=200:
        args = [arg.strip() for arg in val.args.split(',')] if val.args else 1
        print(val.url,args)
        try:
            db_entrys = filter_entrys(request.json(),val.tag,val.value)
            if db_entrys:
                try:
                    for entry in db_entrys:
                        Query.add_values(val.metric_id,entry[0],entry[1],datetime.datetime())
                except:
                    print('writing values failed')
            else:
                print('BAD FORMAT')
                Query.pause_token(val.metric_id)
        except:
            Query.pause_token(val.metric_id)
            print("FILTER FAILED") 
    elif request.status_code == 401:
        Query.pause_token(val.metric_id)
        print('Authentication Error')
    elif request.status_code == 403:
        Query.pause_token(val.metric_id)
        print("URL FORBIDEN OPERATION")
    elif request.status_code == 404:
        Query.pause_token(val.metric_id)
        print('URL NOT FOUND')
    elif request.status_code < 500:
        print('bad request')
        Query.pause_token(val.metric_id)
    else:
        print('Internal Server Error')
        
    return False
