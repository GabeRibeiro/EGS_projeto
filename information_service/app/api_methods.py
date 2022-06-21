from flask import Flask, request, jsonify
import mysql.connector
from flaskext.mysql import MySQL
from flask_restful import Api,Resource,reqparse,abort
import json
import requests
from datetime import datetime
from functools import wraps

app = Flask(__name__)

host = ""
user = ""
password = ""
dbport = ""
database = ""
verify_url = ""

with open("/tmp/secrets/AUTHSERVICE_VERIFY_URL", 'r') as f:
    verify_url = f.read()

with open("/tmp/secrets/password", 'r') as f:
    password = f.read()
app.config["MYSQL_DATABASE_PASSWORD"] = password

with open("/tmp/secrets/host", 'r') as f:
    host = f.read()

with open("/tmp/secrets/user", 'r') as f:
    user = f.read()

with open("/tmp/secrets/dbport", 'r') as f:
    dbport = f.read()

with open("/tmp/secrets/database", 'r') as f:
    database = f.read()

db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
cursor = db.cursor()

api = Api(app)

# __________________________ DB QUERYS _____________________________
class Query:
    def last_insertedID():
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        cursor.execute('SELECT MAX(metric_id) FROM Basic_url')
        values = (cursor.fetchall())[0]
        cursor.close()
        db.close()
        return values

    def add_basic(url,user_id,value,tag,period,status,auth_type):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = 'INSERT INTO Basic_url (url,user_id,value,tag,period,status,auth_type) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        val = (url,user_id,value,tag,period,status,auth_type)
        cursor.execute(sql,val)
        db.commit()       
        cursor.close()
        db.close()

    def add_key(parent_id,key):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = 'INSERT INTO Key_url (parent_id,secret_key) VALUES (%s,%s)'
        val = (parent_id,key)
        cursor.execute(sql,val)
        db.commit()
        cursor.close()
        db.close()
    def add_http(parent_id,key,username):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = 'INSERT INTO Http_url (parent_id,secret_key,username) VALUES (%s,%s,%s)'
        val = (parent_id,key,username)
        cursor.execute(sql,val)
        db.commit()
        cursor.close()
        db.close()
    def add_token(parent_id,token_url,key,secret,content_type,auth_type):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = 'INSERT INTO Token_url (parent_id,token_url,secret_key,secret,content_type,auth_type) VALUES (%s,%s,%s,%s,%s,%s)'
        val = (parent_id,token_url,key,secret,content_type,auth_type)
        cursor.execute(sql,val)
        db.commit()
        cursor.close()
        db.close()

    def get_urls():
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        cursor.execute("SELECT * FROM Basic_url")
        values = cursor.fetchall()
        cursor.close()
        db.close()
        return values
    def get_url(url,user_id):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = 'SELECT * FROM Basic_url WHERE user_id = %s AND url= %s'
        val = [user_id,url]
        cursor.execute(sql,val)
        values = cursor.fetchall()
        cursor.close()
        db.close()
        return values
    def get_urls_info(user_id):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = '''
                SELECT * FROM Basic_url WHERE user_id = %s 
              '''
        val = [user_id]
        cursor.execute(sql,val)
        values = []
        values.extend(cursor.fetchall())
        
        sql = '''
                SELECT Basic_url.metric_id,url,value,tag,period,status,secret_key FROM Basic_url,Key_url WHERE user_id = %s AND parent_id = Basic_url.metric_id 
              '''
        cursor.execute(sql,val)
        values.extend(cursor.fetchall())

        sql = '''
                SELECT Basic_url.metric_id,url,value,tag,period,status,username,secret_key FROM Basic_url,Http_url WHERE user_id = %s AND parent_id = Basic_url.metric_id 
              '''
        cursor.execute(sql,val)
        values.extend(cursor.fetchall())

        sql = '''
                SELECT Basic_url.metric_id,url,value,tag,period,status,token_url,secret_key,secret,content_type,Token_url.auth_type FROM Basic_url,Token_url WHERE user_id = %s AND parent_id = Basic_url.metric_id
              '''
        cursor.execute(sql,val)
        values.extend(cursor.fetchall())
        
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
        cursor.execute("USE "+database)
        sql = 'SELECT * FROM Basic_url WHERE period = %s and user_id = %s'
        val = (freq,user_id)
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
        cursor.execute("USE "+database)
        sql = 'SELECT Value.timestamp,Value.tag,Value.value FROM Basic_url WHERE period = %s AND status = 1'
        val = [freq]
        cursor.execute(sql,val)
        values = cursor.fetchall()
        cursor.close()
        db.close()
        return values
    
    # verificar se o user tem acesso aos urls
    def get_url_data(user_id,id,tag,lower_limit,upper_limit):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = 'SELECT * FROM Value,Basic_url WHERE Basic_url.user_id=%s AND Basic_url.metric_id=%s AND Value.tag=%s AND timestamp >= %s AND timestamp <= %s'
        val = (user_id,id,tag,lower_limit, upper_limit)
        cursor.execute(sql,val)
        values = cursor.fetchall()
        cursor.close()
        db.close()
        return values

    def remove_basic(metric_id,user_id):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = 'DELETE FROM Basic_url WHERE metric_id = %s AND user_id = %s'
        val = (metric_id,user_id)
        cursor.execute(sql,val)
        db.commit()
        cursor.close()
        db.close()
    
    
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
    def change_basic(metric_id,db_type,user_id):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = "UPDATE Basic_url SET "
        for key in db_type:
            sql += key + ' = ' + str(db_type[key])+','
        sql = sql[:-1]  # remove last ','
        sql += ' WHERE metric_id = ' + metric_id + ' AND user_id = '+user_id+';'
        print('___________________________________\n\n\n')
        print(sql)
        print('___________________________________\n\n\n')
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
    def change_key(metric_id,db_type,user_id):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = "UPDATE Key_url SET "
        for key in db_type:
            sql += key + '=' + str(db_type[key])+','
        sql = sql[:-1]  # remove last ','
        sql += ' WHERE metric_id = ' + metric_id + ' and user_id='+user_id  
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
    def change_http(metric_id,db_type,user_id):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = "UPDATE Http_url SET "
        for key in db_type:
            sql += key + '=' + str(db_type[key])+','
        sql = sql[:-1]  # remove last ','
        sql += ' WHERE metric_id = ' + metric_id + ' and user_id = '+user_id 
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
    def change_token(metric_id,db_type,user_id):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        sql = "UPDATE Token_url SET "
        for key in db_type:
            sql += key + '=' + str(db_type[key])+','
        sql = sql[:-1]  # remove last ','
        sql += ' WHERE metric_id = ' + metric_id + ' and user_id = '+user_id  
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

    def check_basics_id(metric_id):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        val = [metric_id]
        sql = 'SELECT * FROM Basic_url WHERE metric_id = %s'
        cursor.execute(sql,val)
        values = cursor.fetchall()
        
        cursor.close()
        db.close()
        return values

    def get_tags(metric_id,user_id):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
        cursor = db.cursor()
        cursor.execute("USE "+database)
        val = [metric_id,user_id]
        sql = 'SELECT tag FROM Basic_url WHERE metric_id = %s AND user_id = %s'
        cursor.execute(sql,val)
        values = cursor.fetchall()
        
        cursor.close()
        db.close()
        return values

 
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Token is missing'}),403
        
        val = requests.get(verify_url,headers={"auth-token":token})
        if val.status_code != 200:
            return jsonify({'message': 'Token is invalid'}),403
        
        return f(*args, **kwargs)
    return decorated

# ____________________________ BASIC __________________________________
@app.route('/URL/Add/Basic', methods=['PUT'])
@token_required
def api_add_URL_Basic():
    if not request.form.get('url'):
        return "Missing [url] Argument",400
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if not request.form.get('user_id'):
        return "Missing [user_id] Argument",400
    if not request.form.get('tag'):
        return "Missing [tag] Argument",400
    if not request.form.get('value'):
        return "Missing [value] Argument",400
    
    period = 5 if not request.form.get('period') else request.form.get('period')

    Query.add_basic(request.form.get('url'),request.form.get('user_id'),request.form.get('value'),request.form.get('tag'),period,True,'open')
    id = Query.last_insertedID()[0]
    print("ID -> ", id)
    
    return "URL RUNNING!",201

# ____________________________ KEY __________________________________
@app.route('/URL/Add/Key', methods=['PUT'])
@token_required
def api_add_URL_key():
    if not request.form.get('url'):
        return "Missing [url] Argument",400
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if not request.form.get('key'):
        return "Missing [key] Argument",400
    if not request.form.get('tag'):
        return "Missing [tag] Argument",400
    if not request.form.get('value'):
        return "Missing [value] Argument",400 
        
    period = 5 if not request.form.get('period') else request.form.get('period')
    
    Query.add_basic(request.form.get('url'),request.form.get('user_id'),request.form.get('value'),request.form.get('tag'),period,True,'key')    
    
    id = Query.last_insertedID()[0]
    Query.add_key(id,request.form.get('key'))
    
    return "URL RUNNING!",201

# ______________________________ HTTP __________________________________
@app.route('/URL/Add/Http', methods=['PUT'])
@token_required
def api_add_URL_http():
    if not request.form.get('url'):
        return "Missing [url] Argument",400
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if not request.form.get('key'):
        return "Missing [key] Argument",400
    if not request.form.get('username'): 
        return 'Missing [username] Argument',400
    if not request.form.get('tag'):
        return "Missing [tag] Argument",400
    if not request.form.get('value'):
        return "Missing [value] Argument",400 
    
    period = 5 if not request.form.get('period') else request.form.get('period')
    
    Query.add_basic(request.form.get('url'),request.form.get('user_id'),request.form.get('value'),request.form.get('tag'),period,True,'http')
    

    id = Query.last_insertedID()[0]
    Query.add_http(id,request.form.get('username'),request.form.get('key'))
    
    return "URL RUNNING!",201

# ______________________________Token __________________________________

@app.route('/URL/Add/Token', methods=['PUT'])
@token_required
def api_add_URL_Token():
    #if not request.form.get('metric_id'):
    #    return "Missing [id] Argument",400
    if not request.form.get('url'):
        return "Missing [url] Argument",400
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if not request.form.get('token_url'):
        return "Missing [token_url] Argument",400
    if not request.form.get('key'):
        return "Missing [key] Argument",400
    if not request.form.get('secret'):
        return "Missing [secret] Argument",400
    if not request.form.get('content_type'):
        return "Missing [content_type] Argument",400
    if not request.form.get('auth_type'):
        return "Missing [auth_type] Argument",400
    if not request.form.get('tag'):
        return "Missing [tag] Argument",400
    if not request.form.get('value'):
        return "Missing [value] Argument",400
    
    period = 5 if not 'period' in request.form.get('period') else request.form.get('period')
    
    Query.add_basic(request.form.get('url'),request.form.get('user_id'),request.form.get('value'),request.form.get('tag'),period,True,'token')

    id = Query.last_insertedID()[0]
    Query.add_token(id,request.form.get('token_url'),request.form.get('key'),request.form.get('secret'),request.form.get('content_type'),request.form.get('auth_type'))

    return "URL RUNNING!",201


@app.route('/URL/Pause',methods=['POST'])
@token_required 
def api_pause_basic():
    if not request.form.get('metric_id'):
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.form.get('metric_id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    
    Query.change_basic(request.form.get('metric_id'),{'status':False},request.form.get('user_id'))
    return "URL PAUSED",201

@app.route('/URL/Start',methods=['POST'])
@token_required 
def api_start_basic():
    
    if not request.form.get('metric_id'):
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.form.get('metric_id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    
    Query.change_basic(request.form.get('metric_id'),{'status':True},request.form.get('user_id'))
    return "URL STARTED",201

@app.route('/URL/Remove', methods=['POST'])
@token_required
def api_remove_basic():
    if not request.form.get('metric_id'):
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.form.get('metric_id')):        
        return 'URL id NOT FOUND',403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    
    Query.remove_basic(request.form.get('metric_id'),request.form.get('user_id'))
    return 'URL REMOVED',201

@app.route('/URL/Update/Basic',methods=['POST'])
@token_required 
def api_update_basic():
    if not request.form.get('metric_id'):
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.form.get('metric_id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    values = {}
    for db_type in [val for val in request.form.args if val!='metric_id']: 
        values[db_type] = request.form.get(db_type)
    Query.change_basic(request.form.get('metric_id'),values,request.form.get('user_id'))
    return "URL STARTED",201

@app.route('/URL/Update/Key',methods=['POST'])
@token_required 
def api_update_key():
    if not request.form.get('metric_id'):
        return 'Missing [id] Argument',400
    if not Query.check_keys_id(request.form.get('metric_id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    values = {}
    for db_type in [val for val in request.form.args if val!='metric_id']: 
        values[db_type] = request.form.get(db_type)
    Query.change_key(request.form.get('metric_id'),values,request.form.get('user_id'))
    return "URL STARTED",201

@app.route('/URL/Update/Http',methods=['POST'])
@token_required 
def api_update_http():
    if not request.form.get('metric_id'):
        return 'Missing [id] Argument',400
    if not Query.check_http_id(request.form.get('metric_id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    values = {}
    for db_type in [val for val in request.form.args if val!='metric_id']: 
        values[db_type] = request.form.get(db_type)
    Query.change_http(request.form.get('metric_id'),values,request.form.get('user_id'))
    return "URL STARTED",201

@app.route('/URL/Update/Token',methods=['POST'])
@token_required 
def api_update_token():
    if not request.form.get('metric_id'):
        return 'Missing [id] Argument',400
    if not Query.check_token_id(request.form.get('metric_id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    values = {}
    for db_type in [val for val in request.form.args if val!='metric_id']: 
        values[db_type] = request.form.get(db_type)
    Query.change_token(request.form.get('metric_id'),values,request.form.get('user_id'))
    return "URL STARTED",201

@app.route('/URL/Period/<int:period>',methods=['GET'])
@token_required 
def api_period_basic(period):
    if not 'user_id' in request.args.keys(): 
        return 'Missing [user_id] Argument',400
    return json.dumps(Query.get_basic_period(period,request.args['user_id'])),201

@app.route('/URL/All',methods=['GET'])
@token_required 
def api_all():
    if not 'user_id' in request.args.keys(): 
        return 'Missing [user_id] Argument',400
    data = Query.get_urls_info(request.args['user_id'])
    return json.dumps(data),201
    
@app.route('/URL/Search/URL',methods=['GET'])
@token_required 
def api_url():
    if not 'user_id' in request.args.keys(): 
        return 'Missing [user_id] Argument',400
    if not 'url' in request.args.keys(): 
        return 'Missing [url] Argument',400
    data = Query.get_url(request.args['url'],request.args['user_id'])
    return json.dumps(data),201

@app.route('/URL/Filter/Interval',methods=['GET'])
@token_required 
def api_interval():
    if not 'metric_id' in request.args.keys(): 
        return 'Missing [metric_id] Argument',400
    if not 'user_id' in request.args.keys(): 
        return 'Missing [user_id] Argument',400
    if not 'lower_limit' in request.args.keys():
        return 'Missing [lower_limit] Argument',400
    if not 'upper_limit' in request.args.keys():
        return 'Missing [upper_limit] Argument',400
    if not 'tag' in request.args.keys():
        return 'Missing [tag] Argument',400
    
    data = Query.get_url_data(request.args['user_id'],request.args['metric_id'],request.args['tag'],request.args['lower_limit'],request.args['upper_limit'])
    
    return json.dumps(data,default=str),201

@app.route('/URL/Tags',methods=['GET'])
@token_required 
def api_tags():
    if not 'metric_id' in request.args.keys(): 
        return 'Missing [metric_id] Argument',400
    if not 'user_id' in request.args.keys(): 
        return 'Missing [user_id] Argument',400

    data = Query.get_tags(request.args['metric_id'],request.args['user_id'])

    return json.dumps(data,default=str),201
"""
@app.route('/URL/Cheat',methods=['GET'])
@token_required 
def api_cheat():
    db = mysql.connector.connect(
            host=host,
            user=user,
            password = password,
            port = dbport,
            database = database
        )
    cursor = db.cursor()
    cursor.execute("USE "+database)
    cursor.execute(request.args['sql'])
    values = cursor.fetchall()
    cursor.close()
    db.close()
    return json.dumps(values,default=str),201
"""

"""
@app.route('/URL/Print', methods=['GET'])
@token_required
def api_print_basics():
    urls_info = Query.get_urls()
    for url in urls_info:
        print(url)
    return json.dumps(urls_info),201
"""

@app.route('/',methods=['GET'])
def home():
	return 'URL_API'

if __name__ == "__main__":
    app.run(host="localhost",port=8000,debug=False)