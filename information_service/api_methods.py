from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse,abort
from sqlalchemy.dialects.postgresql import JSON
import json
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
#print(os.environ.get('DATABASE_URL') or \
#        'sqlite:///' + os.path.join(basedir, 'app.db'))
#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
#        'sqlite:///' + os.path.join(basedir, 'URLs_db.db')

#   juntar as tables auth2/http/key/open e os metodos
#   fazer table para args
#   users table
#   id generator
#   querys para valores de args entre certos intervalos de tempo
#   querys para valores superiores/inferiores de args
#   fazer gets para os url's 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_database2.db'
app.config['SECRET_KEY'] = 'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'

db = SQLAlchemy(app)
api = Api(app)
   
    
# ________________________ DB MODELS _______________________________
class Key_url(db.Model):
    __tablename__ = "key_url"
    metric_id = db.Column(db.Integer,primary_key=True)
    parent_id = db.Column(db.Integer,db.ForeignKey('basic_url.metric_id', ondelete="CASCADE"))
    key = db.Column(db.String(300))
    
    #parent = db.relationship("Basic_url", back_populates="key_child")
    
    def __repr__(self):
        return f"API(id={self.metric_id},URL={self.url}, period={self.period},status={self.status}, args={self.args})"
    
class Http_url(db.Model):
    __tablename__ = "http_url"
    metric_id = db.Column(db.Integer,primary_key=True)
    parent_id = db.Column(db.Integer,db.ForeignKey('basic_url.metric_id', ondelete="CASCADE"))
    key = db.Column(db.String(300))
    username = db.Column(db.String(300))
    
    #parent = db.relationship("Basic_url", back_populates="http_child")
    
    def __repr__(self):
        return f"API(id={self.metric_id},URL={self.url}, period={self.period},status={self.status}, args={self.args})"  
    
class Token_url(db.Model):
    __tablename__ = "token_url"
    metric_id = db.Column(db.Integer,primary_key=True)
    parent_id = db.Column(db.Integer,db.ForeignKey('basic_url.metric_id', ondelete="CASCADE"))
    token_url = db.Column(db.String(500),nullable=False)
    key = db.Column(db.String(300))
    secret = db.Column(db.String(300))
    content_type = db.Column(db.String(50))
    auth_type = db.Column(db.String(50))
    
    #parent = db.relationship("Basic_url", back_populates="token_child")
    
    def __repr__(self):
        return f"API(id={self.metric_id},URL={self.url}, period={self.period}, status={self.status}, args={self.args})"

class Value(db.Model):
    __tablename__ = "value"
    url_id = db.Column(db.Integer,db.ForeignKey('basic_url.metric_id', ondelete="CASCADE"))
    timestamp = db.Column(db.DateTime,primary_key=True)
    value = db.Column(db.Float)
    def __repr__(self):
        return f"(value={self.value},timestamp={self.timestamp})"
    
class Basic_url(db.Model):
    __tablename__ = "basic_url"
    metric_id = db.Column(db.Integer(),primary_key=True)
    url = db.Column(db.String(500),nullable=False)
    user_id = db.Column(db.Integer(),unique=True)
    args = db.Column(db.String(750),nullable=True)
    period = db.Column(db.Integer())
    status = db.Column(db.Boolean(),nullable=False,default=True)
    
    #key_child = db.relationship('Key_url', back_populates="parent", cascade="all, delete-orphan", passive_deletes=True)
    #http_child = db.relationship('Http_url', back_populates="parent", cascade="all, delete-orphan", passive_deletes=True)
    #token_child = db.relationship('Token_url', back_populates="parent", cascade="all, delete-orphan", passive_deletes=True)
    
    def __repr__(self):
        return f"API(id={self.metric_id},URL = {self.url}, period={self.period}, status = {self.status}, args={self.args})"
      

db.create_all()
db.session.commit()

# __________________________ DB QUERYS _____________________________
class Query:
    # return basic url's
    def get_url_info(val):
        return db.session.query(Basic_url.args,Basic_url.metric_id).filter(Basic_url.url==val,Basic_url.status==True).all()
    def get_urls():
        return db.session.query(Basic_url.metric_id,Basic_url.url,Basic_url.args,Basic_url.status,Basic_url.period).all()
    def get_url(user_id):
        return db.session.query(Basic_url.metric_id,Basic_url.url,Basic_url.args,Basic_url.status,Basic_url.period).filter(user_id=user_id)
    def get_url_info(user_id):
        return db.session.query(Basic_url).join(Token_url,Http_url,Key_url).filter(Basic_url.user_id==user_id).all()
    def get_token():
        return db.session.query(Token_url.metric_id).all()
   
    def remove_basic(val):
        Basic_url.query.filter(Basic_url.metric_id == val).delete()
        Key_url.query.filter(Key_url.parent_id == val).delete()
        Http_url.query.filter(Http_url.parent_id == val).delete()
        Token_url.query.filter(Token_url.parent_id == val).delete()
        db.session.commit()
   
    def check_basics_id(val):
        return Basic_url.query.filter(Basic_url.metric_id == val).first()
    def check_keys_id(val):
        return Key_url.query.filter(Key_url.metric_id == val).first()
    def check_http_id(val):
        return Http_url.query.filter(Http_url.metric_id == val).first()
    def check_token_id(val):
        return Token_url.query.filter(Token_url.metric_id == val).first()

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
    
    if not request.form.get('id'):
        return "Missing [id] Argument",400
    if not request.form.get('url'):
        return "Missing [url] Argument",400
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if Query.check_basics_id(request.form.get('id')):
        return "id already exists",403
    if not request.form.get('user_id'):
        return "Missing [user_id] Argument",400
    
    aux = None
    if request.form.get('args'):
        aux = request.form.get('args') 
    
    period = 5 if not request.form.get('period') else request.form.get('period')
    
    basic_obj = Basic_url(metric_id=request.form.get('id'),url=request.form.get('url'),args=aux,period=period,status=True,user_id=request.form.get('user_id'))
    db.session.add(basic_obj)
    db.session.commit()
    
    return "URL RUNNING!",201

# ____________________________ KEY __________________________________
@app.route('/URL/Add/Key', methods=['PUT'])
@token_required
def api_add_URL_key():
    if not request.form.get('id'):
        return "Missing [id] Argument",400
    if Query.check_keys_id(request.form.get('id')):
        return 'id already exists',403
    if not request.form.get('url'):
        return "Missing [url] Argument",400
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if not request.form.get('key'):
        return "Missing [key] Argument",400
    
    aux = None
    if request.form.get('args'):
        aux = request.form.get('args') 
        
    period = 5 if not request.form.get('period') else request.form.get('period')
    basic_obj = Basic_url(metric_id=request.form.get('id'),url=request.form.get('url'),args=aux,period=period,status=True,user_id=request.form.get('user_id'))
    db.session.add(basic_obj)
    
    key_obj = Key_url(metric_id=int(request.form.get('id')),parent_id=int(request.form.get('id')),key=request.form.get('key'))
    db.session.add(key_obj)
    db.session.commit()
    
    return "URL RUNNING!",201

# ______________________________ HTTP __________________________________
@app.route('/URL/Add/Http', methods=['PUT'])
@token_required
def api_add_URL_http():
    if not request.form.get('id'):
        return "Missing [id] Argument",400
    if not request.form.get('url'):
        return "Missing [url] Argument",400
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if Query.check_http_id(request.form.get('id')):
        return 'URL id already exists',403
    if not request.form.get('key'):
        return "Missing [key] Argument",400
    if not request.form.get('username'): 
        return 'Missing [username] Argument',400
    
    aux = None
    if request.form.get('args'):
        aux = request.form.get('args') 
    
    period = 5 if not request.form.get('period') else request.form.get('period')
    
    basic_obj = Basic_url(metric_id=request.form.get('id'),url=request.form.get('url'),args=aux,period=period,status=True,user_id=request.form.get('user_id'))
    db.session.add(basic_obj)
    db.session.commit()
    
    http_obj = Http_url(metric_id=int(request.form.get('id')),parent_id=int(request.form.get('id')),key=request.form.get('key'),username=request.form.get('username'))
    db.session.add(http_obj)
    db.session.commit()
    
    return "URL RUNNING!",201

# ______________________________Token __________________________________

@app.route('/URL/Add/Token', methods=['PUT'])
@token_required
def api_add_URL_Token():
    if not request.form.get('id'):
        return "Missing [id] Argument",400
    if not request.form.get('url'):
        return "Missing [url] Argument",400
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    if Query.check_token_id(request.form.get('id')):
        return 'id Already Exists',403
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
      
    aux = None
    if request.form.get('args'):
        aux = request.form.get('args') 
    
    period = 5 if not 'period' in request.form.get('period') else request.form.get('period')
    
    basic_obj = Basic_url(metric_id=request.form.get('id'),url=request.form.get('url'),args=aux,period=period,status=True)
    db.session.add(basic_obj)
    token_obj = Token_url(metric_id=request.form.get('id'),parent_id=request.form.get('id'),token_url=request.form.get('token_url'),key=request.form.get('key'),secret=request.form.get('secret'),content_type=request.form.get('content_type'),auth_type=request.form.get('auth_type'),user_id=request.form.get('user_id'))
    db.session.add(token_obj)
    db.session.commit()
    
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
    
    Query.change_basic(request.form.get('id'),"status",False)
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
    
    Query.change_basic(request.form.get('id'),"status",True)
    return "URL STARTED",201

@app.route('/URL/Print', methods=['GET'])
@token_required
def api_print_basics():
    print(Query.get_urls())
    return "PRINTED",201

@app.route('/URL/Remove', methods=['POST'])
@token_required
def api_remove_basic():
    print(Query.get_token())
    if not request.form.get('id'):
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.form.get('id')):        
        return 'URL id NOT FOUND',403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    
    Query.remove_basic(request.form.get('id'),request.form.get('user_id'))
    
    return 'URL REMOVED',201

@app.route('/URL/Update',methods=['POST'])
@token_required 
def api_update_basic():
    if not request.form.get('id'):
        return 'Missing [id] Argument',400
    if not Query.check_basics_id(request.form.get('id')):
        return "URL id NOT FOUND",403
    if not request.form.get('user_id'): 
        return 'Missing [user_id] Argument',400
    for db_type in [val for val in request.form.args if val!='id']: 
        Query.change_basic(request.form.get('id'),db_type,request.args[db_type],request.form.get('user_id'))
    return "URL STARTED",201

@app.route('/URL/Period/<int:period>',methods=['GET'])
@token_required 
def api_period_basic(period):
    print(Query.get_basic_period(period))
    return "PRINTED URLS FREQ 5",201

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
    
    
    
    return json.dumps(data),201
    
@app.route('/URL/Filter/Higher',methods=['GET'])
@token_required 
def api_higher():
    
@app.route('/URL/Filter/Lower',methods=['GET'])
@token_required 
def api_lower():
    
@app.route('/URL/Filter/Min',methods=['GET'])
@token_required 
def api_min():
    
@app.route('/URL/Filter/Max',methods=['GET'])
@token_required 
def api_max():


@app.route('/',methods=['GET'])
def home():
	return 'URL_API'

if __name__ == "__main__":
    app.run(debug=False)