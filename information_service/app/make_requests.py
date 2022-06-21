import time

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector

from make_requests_utils import *


scheduler = BackgroundScheduler()

host = ""
user = ""
password = ""
dbport = ""
database = ""

with open("/tmp/secrets/password", 'r') as f:
    password = f.read()

with open("/tmp/secrets/host", 'r') as f:
    host = f.read()

with open("/tmp/secrets/user", 'r') as f:
    user = f.read()

with open("/tmp/secrets/dbport", 'r') as f:
    dbport = f.read()

with open("/tmp/secrets/database", 'r') as f:
    database = f.read()

class Query:
    def get_url_request(freq):
        db = mysql.connector.connect(
                host=host,
                user=user,
                password = password,
                port = dbport,
                database = database
            )
        cursor = db.cursor()
        sql = 'SELECT * FROM Basic_url WHERE period = %s'
        val = [freq]
        cursor.execute(sql,val)
        values = cursor.fetchall()
        cursor.close()
        db.close()
        return values
    def get_basic_period(freq,user_id):
        db = mysql.connector.connect(
                host=host,
                user=user,
                password = password,
                port = dbport,
                database = database
            )
        cursor = db.cursor()
        sql = 'SELECT * FROM Basic_url WHERE period = %s and user_id = %s'
        val = (freq,user_id)
        cursor.execute(sql,val)
        values = cursor.fetchall()
        cursor.close()
        db.close()
        return values
    def get_requests_period(freq):
        db = mysql.connector.connect(
                host=host,
                user=user,
                password = password,
                port = dbport,
                database = database
            )
        cursor = db.cursor()
        sql = 'SELECT * FROM Basic_url WHERE period = %s AND status = 1'
        val = [freq]
        cursor.execute(sql,val)
        values = cursor.fetchall()
        cursor.close()
        db.close()
        return values
    def get_basic_args(metric_id):
        db = mysql.connector.connect(
                host=host,
                user=user,
                password = password,
                port = dbport,
                database = database
            )
        cursor = db.cursor()
        sql = 'SELECT args FROM Basic_url WHERE metric_id = %s'
        val = [metric_id]
        cursor.execute(sql,val)
        values = cursor.fetchall()
        cursor.close()
        db.close()
        return values
    def get_basic_period(freq,user_id):
        db = mysql.connector.connect(
                host=host,
                user=user,
                password = password,
                port = dbport,
                database = database
            )
        cursor = db.cursor()
        sql = 'SELECT * FROM Basic_url WHERE period = %s AND status = 1'
        val = [freq]
        cursor.execute(sql,val)
        values = cursor.fetchall()
        cursor.close()
        db.close()
        return values
    def get_key(metric_id):
        db = mysql.connector.connect(
                host=host,
                user=user,
                password = password,
                port = dbport,
                database = database
            )
        cursor = db.cursor()
        sql = 'SELECT * FROM Key_url WHERE parent_id = %s'
        val = [metric_id]
        cursor.execute(sql,val)
        value = (cursor.fetchall())[0]
        cursor.close()
        db.close()
        return value
    def get_http(metric_id):
        db = mysql.connector.connect(
                host=host,
                user=user,
                password = password,
                port = dbport,
                database = database
            )
        cursor = db.cursor()
        sql = 'SELECT * FROM Http_url WHERE parent_id = %s'
        val = [metric_id]
        cursor.execute(sql,val)
        value = (cursor.fetchall())[0]
        cursor.close()
        db.close()
        return value
    def get_token(metric_id):
        db = mysql.connector.connect(
                host=host,
                user=user,
                password = password,
                port = dbport,
                database = database
            )
        cursor = db.cursor()
        sql = 'SELECT * FROM Token_url WHERE parent_id = %s'
        val = [metric_id]
        cursor.execute(sql,val)
        value = (cursor.fetchall())[0]
        cursor.close()
        db.close()
        return value
    def pause_url(metric_id):
        db = mysql.connector.connect(
                host=host,
                user=user,
                password = password,
                port = dbport,
                database = database
            )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = 'UPDATE Basic_url SET status=0 WHERE metric_id = %s'
        val = [metric_id]
        cursor.execute(sql,val)
        db.commit()
        cursor.close()
        db.close()
    def add_value(url_id,tag,value):
        db = mysql.connector.connect(
                host=host,
                user=user,
                password = password,
                port = dbport,
                database = database
            )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = 'INSERT INTO Value (url_id,tag,value) VALUES (%s,%s,%s)'
        val = (url_id,tag,value)
        cursor.execute(sql,val)
        db.commit()
        cursor.close()
        db.close()

def make_request(period):
    for val in Query.get_requests_period(period):
        if val[7] == 'token':
            token_url = Query.get_token(val[0])
            request_token(val[0],val[1],val[3],val[4],token_url[2],token_url[3],token_url[4],token_url[5],token_url[6],val[5])
        elif val[7] == 'http':
            http_url = Query.get_http(val[0])
            request_http(val[0],val[1],val[3],val[4],http_url[3],http_url[2])
        elif val[7] == 'key':
            key_url = Query.get_key(val[0])
            request_key(val[0],val[1],val[3],val[4],key_url[1])
        else:
            request_basic(val[0],val[1],val[3],val[4])

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