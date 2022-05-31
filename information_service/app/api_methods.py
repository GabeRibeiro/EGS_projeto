from flask import Flask, request, jsonify
import mysql.connector
from flaskext.mysql import MySQL
from flask_restful import Api,Resource,reqparse,abort
from config import *
import json
from datetime import datetime
from functools import wraps



app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = Config.URI
app.config['SECRET_KEY'] = Config.key
#app.config['MYSQL_HOST'] = Config.host
#app.config['MYSQL_USER'] = Config.user
#app.config['MYSQL_PASSWORD'] = 'root'
#app.config['MYSQL_DB'] = 'flask'

#db = MySQL()
#db.init_app(app)
#cursor = db.get_db().cursor()

api = Api(app)

#Set mysql access credentials
db = mysql.connector.connect(
  host=Config.host,
  user=Config.user,
  password = Config.password,
  port = Config.port,
  database = Config.database
)

#config = {
#    'host': 'db',
#    'user': 'root',
#    'password': 'root',
#    'port': '3306',
#    'database': 'url_db'
#}
#db = mysql.connector.connect(**config)

#Cursor to access mysql
cursor = db.cursor()
cursor.execute("USE "+Config.database)

# __________________________ DB QUERYS _____________________________
class Query:
    #next_metric_id = 0 if db.session.query(Basic_url).count() == 0 else db.session.query(func.max(Basic_url.metric_id)).scalar()+1
    def last_insertedID():
        cursor.execute('SELECT LAST_INSERT_ID()')
        return cursor.fetchone()
    def add_basic(url,user_id,value,tag,period,status,auth_type):
        sql = 'INSERT INTO Basic_url (url,user_id,value,tag,period,status,auth_type) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        val = (url,user_id,value,tag,period,status,auth_type)
        print("val -> " ,val)
        cursor.execute(sql,val)
        db.commit()
    def add_key(parent_id,key):
        sql = 'INSERT INTO Key_url (parent_id,secret_key) VALUES (%s,%s)'
        val = (parent_id,key)
        cursor.execute(sql,val)
        db.commit()
    def add_http(parent_id,key,username):
        sql = 'INSERT INTO Http_url (parent_id,secret_key,username) VALUES (%s,%s,%s)'
        val = (parent_id,key,username)
        cursor.execute(sql,val)
        db.commit()
    def add_token(parent_id,token_url,key,secret,content_type,auth_type):
        sql = 'INSERT INTO Token_url (parent_id,token_url,secret_key,secret,content_type,auth_type) VALUES (%s,%s,%s,%s,%s,%s)'
        val = (parent_id,token_url,key,secret,content_type,auth_type)
        cursor.execute(sql,val)
        db.commit()
    def add_value(url_id,tag,value):
        sql = 'INSERT INTO Value (url_id,tag,value) VALUES (%s,%s,%s)'
        val = (url_id,tag,value)
        cursor.execute(sql,val)
        db.commit()

    #def get_url_info(user_id):
        #cursor.execute("SELECT * FROM Basic_url WHERE user_id == %d")
        #return cursor.fetchall()
        #return db.session.query(Basic_url.tag,Basic_url.value,Basic_url.metric_id).filter(Basic_url.url==val,Basic_url.status==True).all()
    #    return
    def get_urls():
        cursor.execute("SELECT * FROM Basic_url")
        return cursor.fetchall()
    def get_url(user_id):
        sql = 'SELECT * FROM Basic_url WHERE user_id = %s'
        val = [user_id]
        cursor.execute(sql,val)
        return cursor.fetchall()
        #return db.session.query(Basic_url.metric_id,Basic_url.url,Basic_url.tag,Basic_url.value,Basic_url.status,Basic_url.period).filter(user_id=user_id)
    def get_url_info(user_id):
        sql = 'SELECT * FROM Basic_url,Key_url,Http_url,Token_url WHERE Basic_url.user_id = %d and (Basic_url.metric_id = Token.parent_id OR Basic_url.metric_id = Http_url.parent_id OR Basic_url.metric_id = Key_url.parent_id)'
        val = [user_id]
        cursor.execute(sql,val)
        return cursor.fetchall()
        #return db.session.query(Basic_url).join(Token_url,Http_url,Key_url).filter(Basic_url.user_id==user_id).all()
    #def get_tokens():
    #    return db.session.query(Token_url.metric_id).all()
    #def num_metrics():
    #    return db.session.query(func.max(Basic_url.metric_id))
    
    def get_url_request(freq):
        sql = 'SELECT * FROM Basic_url WHERE period = %s'
        val = [freq]
        cursor.execute(sql,val)
        return cursor.fetchall()
        #return db.session.query(Basic_url).filter(Basic_url.status==True,Basic_url.period==freq).all()
    def get_basic_period(freq,user_id):
        sql = 'SELECT * FROM Basic_url WHERE period = %s and user_id = %s'
        val = (freq,user_id)
        cursor.execute(sql,val)
        return cursor.fetchall()
    """
    def get_requests_period(freq):
        return db.session.query(Basic_url).filter(Basic_url.status==True,Basic_url.period==freq and Basic_url.user_id == user_id).all()
    def get_basic_period(freq,user_id):
        return db.session.query(Basic_url).filter(Basic_url.status==True,Basic_url.period==freq and Basic_url.user_id == user_id).all()
    def get_key(metric_id):
        return db.session.query(Key_url).filter(Key_url.metric_id == metric_id).scalar()
    def get_http(metric_id):
        return db.session.query(Http_url).filter(Http_url.metric_id == metric_id).scalar()
    def get_token(metric_id):
        return db.session.query(Token_url).filter(Token_url.metric_id == metric_id).scalar()
    def get_basic_args(val):
        return db.session.query(Basic_url.tag,Basic_url.value,Basic_url.metric_id).filter(Basic_url.url==val,Basic_url.status==True).all()
    def get_key_period(freq):
        return Key_url.query.filter(Key_url.status==True,Key_url.period==freq).all()
    def get_http_period(freq):
        return Http_url.query.filter(Http_url.status==True,Http_url.period==freq).all()
    def get_token_period(freq):
        return Token_url.query.filter(Token_url.status==True,Token_url.period==freq).all()
    """
    def remove_basic(metric_id,user_id):
        sql = 'DELETE FROM Basic_url WHERE metric_id = %s AND user_id = %s'
        val = (metric_id,user_id)
        cursor.execute(sql,val)
        db.commit()
    
    def change_basic(metric_id,db_type,user_id):
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
    def change_key(metric_id,db_type,user_id):
        sql = "UPDATE Key_url SET "
        for key in db_type:
            sql += key + '=' + str(db_type[key])+','
        sql = sql[:-1]  # remove last ','
        sql += ' WHERE metric_id = ' + metric_id + ' and user_id='+user_id  
        cursor.execute(sql)
        db.commit()
    def change_http(metric_id,db_type,user_id):
        sql = "UPDATE Http_url SET "
        for key in db_type:
            sql += key + '=' + str(db_type[key])+','
        sql = sql[:-1]  # remove last ','
        sql += ' WHERE metric_id = ' + metric_id + ' and user_id = '+user_id 
        cursor.execute(sql)
        db.commit()
    def change_token(metric_id,db_type,user_id):
        sql = "UPDATE Token_url SET "
        for key in db_type:
            sql += key + '=' + str(db_type[key])+','
        sql = sql[:-1]  # remove last ','
        sql += ' WHERE metric_id = ' + metric_id + ' and user_id = '+user_id  
        cursor.execute(sql)
        db.commit()
   
    def check_basics_id(metric_id):
        sql = 'SELECT * FROM Basic_url WHERE metric_id = %s'
        val = [metric_id]
        cursor.execute(sql,val)
        return cursor.fetchall()
        #return Basic_url.query.filter(Basic_url.metric_id == val).first()
    
    #def check_keys_id(val):
    #    return Key_url.query.filter(Key_url.metric_id == val).first()
    #def check_http_id(val):
    #    return Http_url.query.filter(Http_url.metric_id == val).first()
    #def check_token_id(val):
    #    return Token_url.query.filter(Token_url.metric_id == val).first()

    
    # verificar se o user tem acesso aos urls
    def get_url_data(user,id,tag,lower_limit, upper_limit):
        sql = 'SELECT * FROM Value,Basic_url WHERE Basic_url.metric_id=%s AND Basic_url.user_id=%s AND Value.tag=%s AND timestamp <= %s AND timestamp >= %s'
        val = (user,id,tag,lower_limit, upper_limit)
        cursor.execute(sql,val)
        db.commit()
    """
    def get_url_higher(user,limit):
        return db.session.query(Basic_url).filter(Basic_url.user_id==user).join(Value).filter(Value.value >= limit)
    def get_url_lower(user,limit):
        return db.session.query(Basic_url).filter(Basic_url.user_id==user).join(Value).filter(Value.value <= limit)
    def get_url_max(user):
        return db.session.query(Value.url_id,func.max(Value.value)).filter()
    def get_url_min(user):
        return db.session.query(Value.url_id,func.min(Value.value)).filter()
    """
    #def add_values(url_id,tag,value):
    #    value_obj = Value(url_id=url_id,value=float(value),tag=tag)
    #    db.session.add(value_obj)
    #    db.session.commit()
 
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Token is missing'}),403
        if token != app.secret_key:
            return jsonify({'message': 'Token is invalid'}),403
        
        """
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'}),403         
        """
        
        return f(*args, **kwargs)
    return decorated

# ____________________________ BASIC __________________________________
@app.route('/URL/Add/Basic', methods=['PUT'])
@token_required
def api_add_URL_Basic():
    
    #if not request.form.get('id'):
    #    return "Missing [id] Argument",400
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
            
    #basic_obj = Basic_url(auth_type='open',metric_id=Query.next_metric_id,url=request.form.get('url'),value=request.form.get('value'),tag=request.form.get('tag'),period=period,status=True,user_id=request.form.get('user_id'))
    #db.session.add(basic_obj)
    #db.session.commit()

    Query.add_basic(request.form.get('url'),request.form.get('user_id'),request.form.get('value'),request.form.get('tag'),period,True,'open')
    id = Query.last_insertedID()[0]
    print("ID -> ", id)
    #Query.next_metric_id+=1
    
    return "URL RUNNING!",201

# ____________________________ KEY __________________________________
@app.route('/URL/Add/Key', methods=['PUT'])
@token_required
def api_add_URL_key():
    #if not request.form.get('id'):
    #    return "Missing [id] Argument",400
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
    
    #id = (int)(Query.num_metrics())+1
    #basic_obj = Basic_url(auth_type='key',metric_id=Query.next_metric_id,url=request.form.get('url'),value=request.form.get('value'),tag=request.form.get('tag'),period=period,status=True,user_id=request.form.get('user_id'))
    #db.session.add(basic_obj)
    Query.add_basic(request.form.get('url'),request.form.get('user_id'),request.form.get('value'),request.form.get('tag'),period,True,'open')    
    
    id = Query.last_insertedID()[0]
    Query.add_key(id,request.form.get('key'))
    #key_obj = Key_url(metric_id=Query.next_metric_id,parent_id=request.form.get('id'),key=request.form.get('key'))
    #db.session.add(key_obj)
    #db.session.commit()
    
    #Query.next_metric_id+=1
    
    return "URL RUNNING!",201

# ______________________________ HTTP __________________________________
@app.route('/URL/Add/Http', methods=['PUT'])
@token_required
def api_add_URL_http():
    #if not request.form.get('id'):
    #    return "Missing [id] Argument",400
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
    
    #id = (int)(Query.num_metrics())+1
    
    #basic_obj = Basic_url(auth_type='http',metric_id=Query.next_metric_id,url=request.form.get('url'),value=request.form.get('value'),tag=request.form.get('tag'),period=period,status=True,user_id=request.form.get('user_id'))
    #db.session.add(basic_obj)
    #db.session.commit()
    Query.add_basic(request.form.get('url'),request.form.get('user_id'),request.form.get('value'),request.form.get('tag'),period,True,'open')
    

    id = Query.last_insertedID()[0]
    Query.add_http(id,request.form.get('username'),request.form.get('key'))
    #http_obj = Http_url(metric_id=Query.next_metric_id,parent_id=request.form.get('id'),key=request.form.get('key'),username=request.form.get('username'))
    #db.session.add(http_obj)
    #db.session.commit()
    
    #Query.next_metric_id+=1
    
    return "URL RUNNING!",201

# ______________________________Token __________________________________

@app.route('/URL/Add/Token', methods=['PUT'])
@token_required
def api_add_URL_Token():
    #if not request.form.get('id'):
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
    
    #id = (int)(Query.num_metrics())+1
    
    #basic_obj = Basic_url(auth_type='token',metric_id=Query.next_metric_id,url=request.form.get('url'),value=request.form.get('value'),tag=request.form.get('tag'),period=period,status=True,user_id=request.form.get('user_id'))
    #db.session.add(basic_obj)
    Query.add_basic(request.form.get('url'),request.form.get('user_id'),request.form.get('value'),request.form.get('tag'),period,True,'open')

    id = Query.last_insertedID()[0]
    Query.add_token(id,request.form.get('token_url'),request.form.get('key'),request.form.get('secret'),request.form.get('content_type'),request.form.get('auth_type'))
    #token_obj = Token_url(metric_id=Query.next_metric_id,parent_id=request.form.get('id'),token_url=request.form.get('token_url'),key=request.form.get('key'),secret=request.form.get('secret'),content_type=request.form.get('content_type'),auth_type=request.form.get('auth_type'))
    #db.session.add(token_obj)
    #db.session.commit()
    
    #Query.next_metric_id+=1
    return "URL RUNNING!",201


@app.route('/URL/Pause',methods=['POST'])
@token_required 
def api_pause_basic():
    if not request.form.get('id'):
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.form.get('id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    
    Query.change_basic(request.form.get('id'),{'status':False},request.form.get('user_id'))
    return "URL PAUSED",201

@app.route('/URL/Start',methods=['POST'])
@token_required 
def api_start_basic():
    
    if not request.form.get('id'):
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.form.get('id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    
    Query.change_basic(request.form.get('id'),{'status':True},request.form.get('user_id'))
    return "URL STARTED",201

@app.route('/URL/Print', methods=['GET'])
@token_required
def api_print_basics():
    print(Query.get_urls())
    for url in Query.get_url:
        print(url.metric_id)
    return "PRINTED",201

@app.route('/URL/Remove', methods=['POST'])
@token_required
def api_remove_basic():
    if not request.form.get('id'):
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.form.get('id')):        
        return 'URL id NOT FOUND',403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    
    #Query.remove_basic(request.form.get('id'),request.form.get('user_id'))
    return 'URL REMOVED',201

@app.route('/URL/Update/Basic',methods=['POST'])
@token_required 
def api_update_basic():
    if not request.form.get('id'):
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.form.get('id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    values = {}
    for db_type in [val for val in request.form.args if val!='id']: 
        values[db_type] = request.form.get(db_type)
    Query.change_basic(request.form.get('id'),values,request.form.get('user_id'))
    return "URL STARTED",201

@app.route('/URL/Update/Key',methods=['POST'])
@token_required 
def api_update_key():
    if not request.form.get('id'):
        return 'Missing [id] Argument',400
    if not Query.check_keys_id(request.form.get('id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    values = {}
    for db_type in [val for val in request.form.args if val!='id']: 
        values[db_type] = request.form.get(db_type)
    Query.change_key(request.form.get('id'),values,request.form.get('user_id'))
    return "URL STARTED",201

@app.route('/URL/Update/Http',methods=['POST'])
@token_required 
def api_update_http():
    if not request.form.get('id'):
        return 'Missing [id] Argument',400
    if not Query.check_http_id(request.form.get('id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    values = {}
    for db_type in [val for val in request.form.args if val!='id']: 
        values[db_type] = request.form.get(db_type)
    Query.change_http(request.form.get('id'),values,request.form.get('user_id'))
    return "URL STARTED",201

@app.route('/URL/Update/Token',methods=['POST'])
@token_required 
def api_update_token():
    if not request.form.get('id'):
        return 'Missing [id] Argument',400
    if not Query.check_token_id(request.form.get('id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    values = {}
    for db_type in [val for val in request.form.args if val!='id']: 
        values[db_type] = request.form.get(db_type)
    Query.change_token(request.form.get('id'),values,request.form.get('user_id'))
    return "URL STARTED",201

@app.route('/URL/Period/<int:period>',methods=['GET'])
@token_required 
def api_period_basic(period):
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    
    return json.dumps(Query.get_basic_period(period,request.form.get('user_id'))),201

@app.route('/URL/All',methods=['GET'])
@token_required 
def api_all():
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    data = Query.get_urls_id(request.form.get('user_id'))
    return json.dumps(data),201
    
@app.route('/URL/Search/URL',methods=['GET'])
@token_required 
def api_url():
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if not request.form.get('url'): 
        return 'Missing [url] Argument',400
    data = Query.get_url(request.form.get('url'),request.form.get('user_id'))
    return json.dumps(data),201

@app.route('/URL/Filter/Interval',methods=['GET'])
@token_required 
def api_interval():
    if not request.form.get('metric_id'): 
        return 'Missing [metric_id] Argument',400
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if not request.form.get('lower_limit'):
        return 'Missing [lower_limit] Argument',400
    if not request.form.get('upper_limit'):
        return 'Missing [upper_limit] Argument',400
    if not request.form.get('tag'):
        return 'Missing [tag] Argument',400
    
    data = Query.get_url_data(request.form.get('user_id'),request.form.get('metric_id'),request.form.get('tag'),request.form.get('lower_limit'),request.form.get('upper_limit'))
    
    return json.dumps(data),201
    
@app.route('/URL/Filter/Higher',methods=['GET'])
@token_required 
def api_higher():
    if not request.form.get('metric_id'): 
        return 'Missing [metric_id] Argument',400
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if not request.form.get('limit'):
        return 'Missing [limit] Argument',400
    
    data = Query.get_url_data_higher(request.form.get('user_id'),request.form.get('metric_id'),request.form.get('limit'))
    
    return json.dumps(data),201
    
@app.route('/URL/Filter/Lower',methods=['GET'])
@token_required 
def api_lower():
    if not request.form.get('metric_id'): 
        return 'Missing [metric_id] Argument',400
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if not request.form.get('limit'):
        return 'Missing [limit] Argument',400
    
    data = Query.get_url_data_lower(request.form.get('user_id'),request.form.get('metric_id'),request.form.get('limit'))
    
    return json.dumps(data),201
    
@app.route('/URL/Filter/Min',methods=['GET'])
@token_required 
def api_min():
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    
    data = Query.get_url_data_min(request.form.get('user_id'))
    
    return json.dumps(data),201

@app.route('/URL/Filter/Max',methods=['GET'])
@token_required 
def api_max():
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    
    data = Query.get_url_data_max(request.form.get('user_id'))
    
    return json.dumps(data),201

@app.route('/',methods=['GET'])
def home():
	return 'URL_API'

if __name__ == "__main__":
    app.run(debug=True)