
from flask import Flask, render_template, request, redirect, Response, make_response

import requests as api_calls

app = Flask(__name__, static_folder='build/static', template_folder='build')


@app.route('/', methods=['GET'])
def get_index():
  
  token = request.args.get('auth-token')

  # check if theres authentication header
  if token == None:
    return redirect('cd')
    
  # check if the token is valid with Authentication Api
  # valid = api_calls.post('http://ratecheck.auth.k3s//validate',
  #   headers={'auth-token': request.headers['auth-token']})  
  
  # if valid.status_code != 200:
  #   return Response(status=403)
  
  res = make_response(render_template('index.html'))
  res.set_cookie('jwt_token', token )
  

  return res
  


    
  