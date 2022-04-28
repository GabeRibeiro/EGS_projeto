import time
import threading

from datetime import datetime
from influxdb import InfluxDBClient
from apscheduler.schedulers.background import BackgroundScheduler
from api_daemon import Query
from make_requests_utils import *

influx = InfluxDBClient(host='40.68.96.164', port=8086, username="peikpis", password="peikpis_2021")
scheduler = BackgroundScheduler()

basic_scheduelers = {'5':1,'15':1,'30':1,'60':1,'1440':1}
key_scheduelers = {'5':1,'15':1,'30':1,'60':1,'1440':1}
http_scheduelers = {'5':1,'15':1,'30':1,'60':1,'1440':1}
token_scheduelers = {'5':1,'15':1,'30':1,'60':1,'1440':1}

def make_request(period):
    
    for val in Query.get_basic_period(period):
        request_basic(val[0])
        
    
    for val in Query.get_key_period(period): 
        request_key(val)
        
        
    for val in Query.get_http_period(period):
        request_http(val)
    
      
    for val in Query.get_token_period(period):
        request_token(val)
     

def start_requests_basic(period,request_id):
    threads = []
    count = 0
    for val in Query.get_basic_period(period):
        count += 1
        if count >= period*(request_id-1) and count < period*request_id:
            threading.Thread(target=request_basic(val[0]))
        elif request_id+1 > basic_scheduelers[str(period)] and count+1 > period*request_id:
            print('new basic added!',request_id+1)
            add_new_basic(period,request_id+1)
            break
    
    for thread in threads:
        thread.join()
        
    if count == 0 and request_id>1:
        remove_basic(period,request_id)

def start_requests_key(period,request_id):
    threads = []
    count = 0
    for val in Query.get_key_period(period):
        count += 1
        if count >= period*(request_id-1) and count < period*request_id:
            print('thread_added',val.metric_id,request_id)
            threading.Thread(target=request_key(val))
        elif request_id+1 > key_scheduelers[str(period)] and count+1 > period*request_id:
            print('new key added!',request_id+1)
            add_new_key(period,request_id+1)
            break
    
    for thread in threads:
        thread.join()
    
    if count == 0 and request_id>1:
        remove_key(period,request_id)

def start_requests_http(period,request_id):
    threads = []
    count = 0
    for val in Query.get_http_period(period):
        count += 1
        if count >= period*(request_id-1) and count < period*request_id:
            print('thread_added',val.metric_id,request_id)
            threading.Thread(target=request_http(val))
        elif request_id+1 > http_scheduelers[str(period)] and count+1 > period*request_id:
            print('new http added!',request_id+1)
            add_new_http(period,request_id+1)
            break
    
    for thread in threads:
        thread.join()
    if count == 0 and request_id>1:
        remove_http(period,request_id)

def start_requests_token(period,request_id):
    threads = []
    count = 0
    for val in Query.get_token_period(period):
        count += 1
        if count >= period*(request_id-1) and count < period*request_id:
            print('thread_added',val.metric_id,request_id)
            threading.Thread(target=request_token(val))
        elif request_id+1 > token_scheduelers[str(period)] and count+1 > period*request_id:
            print('new token added!',request_id+1)
            add_new_token(period,request_id+1)
            break    
    
    for thread in threads:
        thread.join()
    print(count)
    if count == 0 and request_id>1:
        remove_token(period,request_id)


def add_new_basic(period,request_id):
    basic_scheduelers[str(period)] += 1
    scheduler.add_job(start_requests_basic, trigger="interval", args=[period,request_id], minutes=period, id=str(period)+"minjob_basic"+str(request_id), next_run_time=datetime.now())
   

def add_new_key(period,request_id):
    key_scheduelers[str(period)] += 1
    scheduler.add_job(start_requests_key, trigger="interval", args=[period,request_id], minutes=period, id=str(period)+"minjob_key"+str(request_id), next_run_time=datetime.now())
    

def add_new_http(period,request_id):
    http_scheduelers[str(period)] += 1
    scheduler.add_job(start_requests_http, trigger="interval", args=[period,request_id], minutes=period, id=str(period)+"minjob_http"+str(request_id), next_run_time=datetime.now())
  

def add_new_token(period,request_id):
    token_scheduelers[str(period)] += 1
    scheduler.add_job(start_requests_token, trigger="interval", args=[period,request_id], minutes=period, id=str(period)+"minjob_token"+str(request_id), next_run_time=datetime.now())



def remove_basic(period,request_id):
    basic_scheduelers[str(period)] += 1
    scheduler.remove_job(str(period)+"minjob_basic"+str(request_id))
   
def remove_key(period,request_id):
    key_scheduelers[str(period)] += 1
    scheduler.remove_job(str(period)+"minjob_key"+str(request_id))
    

def remove_http(period,request_id):
    http_scheduelers[str(period)] += 1
    scheduler.remove_jobremove_job(str(period)+"minjob_http"+str(request_id))
  

def remove_token(period,request_id):
    token_scheduelers[str(period)] += 1
    scheduler.remove_job(str(period)+"minjob_token"+str(request_id))

def main():
    
    print('STARTING ...')
    print('_____________________________________________________')
    print('Basic\n')
    print(Query.get_basics())
    print('\n')
    print('_____________________________________________________')
    print('Key\n')
    print(Query.get_keys())
    print('\n')
    print('_____________________________________________________')
    print('Http\n')
    print(Query.get_https())
    print('\n')
    print('_____________________________________________________')
    print('Token\n')
    print(Query.get_tokens())
    print('\n')
    print('_____________________________________________________')
    print('\n')
    
    
    job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }
    scheduler.configure(job_defaults=job_defaults)
    
    scheduler.add_job(start_requests_basic, trigger="interval", args=[5,1], minutes=5, id="5minjob_basic", next_run_time=datetime.now())
    scheduler.add_job(start_requests_basic, trigger="interval", args=[15,1], minutes=15, id="15minjob_basic", next_run_time=datetime.now())
    scheduler.add_job(start_requests_basic, trigger="interval", args=[30,1], minutes=30, id="30minjob_basic", next_run_time=datetime.now())
    scheduler.add_job(start_requests_basic, trigger="interval", args=[60,1], minutes=60, id="60minjob_basic", next_run_time=datetime.now())
    scheduler.add_job(start_requests_basic, trigger="interval", args=[1440,1], minutes=1440, id="dailyjob_basic", next_run_time=datetime.now())

    scheduler.add_job(start_requests_key, trigger="interval", args=[5,1], minutes=5, id="5minjob_key", next_run_time=datetime.now())
    scheduler.add_job(start_requests_key, trigger="interval", args=[15,1], minutes=15, id="15minjob_key", next_run_time=datetime.now())
    scheduler.add_job(start_requests_key, trigger="interval", args=[30,1], minutes=30, id="30minjob_key", next_run_time=datetime.now())
    scheduler.add_job(start_requests_key, trigger="interval", args=[60,1], minutes=60, id="60minjob_key", next_run_time=datetime.now())
    scheduler.add_job(start_requests_key, trigger="interval", args=[1440,1], minutes=1440, id="dailyjob_key", next_run_time=datetime.now())

    scheduler.add_job(start_requests_http, trigger="interval", args=[5,1], minutes=5, id="5minjob_http", next_run_time=datetime.now())
    scheduler.add_job(start_requests_http, trigger="interval", args=[15,1], minutes=15, id="15minjob_http", next_run_time=datetime.now())
    scheduler.add_job(start_requests_http, trigger="interval", args=[30,1], minutes=30, id="30minjob_http", next_run_time=datetime.now())
    scheduler.add_job(start_requests_http, trigger="interval", args=[60,1], minutes=60, id="60minjob_http", next_run_time=datetime.now()) 
    scheduler.add_job(start_requests_http, trigger="interval", args=[1440,1], minutes=1440, id="dailyjob_http", next_run_time=datetime.now())  
    
    scheduler.add_job(start_requests_token, trigger="interval", args=[5,1], minutes=5, id="5minjob_token", next_run_time=datetime.now())
    scheduler.add_job(start_requests_token, trigger="interval", args=[15,1], minutes=15, id="15minjob_token", next_run_time=datetime.now())
    scheduler.add_job(start_requests_token, trigger="interval", args=[30,1], minutes=30, id="30minjob_token", next_run_time=datetime.now())
    scheduler.add_job(start_requests_token, trigger="interval", args=[60,1], minutes=60, id="60minjob_token", next_run_time=datetime.now())
    scheduler.add_job(start_requests_token, trigger="interval", args=[1440,1], minutes=1440, id="dailyjob_token", next_run_time=datetime.now())

    scheduler.start()
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("\nexiting...\n")  
        scheduler.shutdown()
if __name__=="__main__":
    main()