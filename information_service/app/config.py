import os
import json
with open('./config.json') as config_file:
	config = json.load(config_file)

#"password": "MySqlPassword1234!",

class Config:

	#SECRET_KEY = config.get('SECRET_KEY')
	user = config.get('user')
	password = config.get('password')
	host = config.get('host')
	apphost = config.get('apphost')
	database = config.get('database')
	URI = config.get('URI')
	port = config.get('port')
	key = config.get('key')
