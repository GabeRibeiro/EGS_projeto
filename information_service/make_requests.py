import time
import threading

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from api_methods import Query
from make_requests_utils import *

scheduler = BackgroundScheduler()

basic_scheduelers = {'5':1,'15':1,'30':1,'60':1,'1440':1}
key_scheduelers = {'5':1,'15':1,'30':1,'60':1,'1440':1}
http_scheduelers = {'5':1,'15':1,'30':1,'60':1,'1440':1}
token_scheduelers = {'5':1,'15':1,'30':1,'60':1,'1440':1}

def make_request(period):
    
    for val in Query.get_requests_period(period):
        if val.auth_type == 'token':
            token_url = Query.get_token(val.auth_type)
            #request_token(val,token_url.token_url,token_url.key,token_url.secret,token_url.content_type,token_url.auth_type)
        elif val.auth_type == 'http':
            http_url = Query.get_http(val.auth_type)
            #request_http(val,http_url.username,http_url.key)
        elif val.auth_type == 'key':
            key_url = Query.get_key(val.auth_type)
            #request_key(val,key_url.key)
        else:
            request_basic(val)

def main():
    
    job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }
    scheduler.configure(job_defaults=job_defaults)
 
    scheduler.add_job(make_request, trigger="interval", args=[5], minutes=5, id="5minjob_token", next_run_time=datetime.now())
    scheduler.add_job(make_request, trigger="interval", args=[15], minutes=15, id="15minjob_token", next_run_time=datetime.now())
    scheduler.add_job(make_request, trigger="interval", args=[30], minutes=30, id="30minjob_token", next_run_time=datetime.now())
    scheduler.add_job(make_request, trigger="interval", args=[60], minutes=60, id="60minjob_token", next_run_time=datetime.now())
    scheduler.add_job(make_request, trigger="interval", args=[1440], minutes=1440, id="dailyjob_token", next_run_time=datetime.now())

    scheduler.start()
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("\nexiting...\n")  
        scheduler.shutdown()
if __name__=="__main__":
    main()