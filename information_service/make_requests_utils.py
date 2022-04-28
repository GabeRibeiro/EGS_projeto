from api_daemon import Query
from utils import *
from make_requests import *
from datetime import datetime as dt

tokens = {}


def format_influx(metric_id,data):
    result = []
    for entry in [entry for entry in data if entry]:
        add_entry = {"measurement":metric_id,"tags":{'id':metric_id}}
        
        if 'Timestamp' in entry:
            add_entry['time'] = dt.fromtimestamp(entry['Timestamp']).isoformat()
            del entry['Timestamp']
        else:
            add_entry['time'] = str(get_timestamp())
        
        for key in [key for key in entry if isinstance(entry[key],str)]:
            add_entry['tags'][key] = entry[key]
            del entry[key]

        if entry:
            add_entry['fields'] = entry
            result.append(add_entry)

    return result 

def request_basic(url):
    print('STARTING BASIC\n')
    request = requests.get(url,timeout=40)
    if request.status_code == 200: 
        for val in Query.get_basic_args(url):
            args = [arg.strip() for arg in val[0].split(',')] if val[0] else 1
            print(url,args)
            try:
                db_entrys = format_influx(val[1],merge_filter(request.json(),args))
                if db_entrys:
                    try:
                        influx.write_points(db_entrys, database="Metrics")
                    except:
                        print('influx failed')
                else:
                    Query.pause_basic(val[1])
                    print('BAD FORMAT BASIC')
            except:
                Query.pause_basic(val[1])
                print("FILTER FAILED")         
    
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

def request_key(val):       
    print('STARTING KEY\n')
    
    request = requests.get(val.url,headers={'Authorization': val.key},timeout=40)
    if request.status_code < 400:
            args = [arg.strip() for arg in val.args.split(',')] if val.args else 1
            print(val.url,args)
            try:
                db_entrys = format_influx(val.metric_id,merge_filter(request.json(),args))
                if db_entrys:
                    try:
                        influx.write_points(db_entrys, database="Metrics")
                    except:
                        print('influx failed')
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

def request_http(val):  
    print('STARTING HTTP\n')
    
    request = requests.get(val.url,headers={"userName": val.username , "password": val.key},timeout=40)
    if request.status_code < 400:    
        args = [arg.strip() for arg in val.args.split(',')] if val.args else 1
        print(val.url,args)
        try:
            db_entrys = format_influx(val.metric_id,merge_filter(request.json(),args))
            print('entrys')
            print(db_entrys)
            print('\n')
            if db_entrys:
                try:
                    influx.write_points(db_entrys, database="Metrics")
                except:
                    print('influx failed')
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
        
def request_token(val):
    print('STARTING TOKEN\n')
    msg = encode_b64(val.key+':'+val.secret)
    
    if val.metric_id in tokens:
        token = tokens[val.metric_id]
    else:
        request = requests.post(val.token_url,headers={'Content-Type': val.content_type, 'Authorization': 'Basic '+msg},timeout=15)
        if request.status_code<300:
            token = val.auth_type + ' ' + request.json()['access_token']
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
        request = requests.post(val.token_url,headers={'Content-Type': val.content_type, 'Authorization': 'Basic '+msg},timeout=15)
        token = val.auth_type + ' ' + request.json()['access_token']
        tokens[val.metric_id] = token
        request = requests.get(val.url,headers={'Authorization': token},timeout=40)
    
    if request.status_code<=200:
        args = [arg.strip() for arg in val.args.split(',')] if val.args else 1
        print(val.url,args)
        try:
            db_entrys = format_influx(val.metric_id,merge_filter(request.json(),args))
            if db_entrys:
                try:
                    influx.write_points(db_entrys, database="Metrics")
                except:
                    print('influx failed')
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
