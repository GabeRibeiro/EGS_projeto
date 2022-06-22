
from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__, static_folder='build/static', template_folder='build')


@app.route('/', methods=['GET'])
def get_index():
  
  token = request.args.get('auth-token')

  # check if theres authentication header
  if token == None:
    return redirect('http://ratecheck-auth.k3s/login')
  
  res = make_response(render_template('index.html'))
  res.set_cookie('jwt_token', token )
  

  return res
  


    
  