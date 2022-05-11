import os
import json
with open('/../etc/config.json') as config_file:
	config = json.load(config_file)

class Config:

	SECRET_KEY = config.get('SECRET_KEY')
	#basedir = os.path.abspath(os.path.dirname(__file__))
	#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        #'sqlite:///' + os.path.join(basedir, 'daemons_database.db')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///daemons_database.db'
