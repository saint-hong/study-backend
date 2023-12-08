# code architecture app.py

import config
from flask import Flask

from sqlalchemy import create_engine 
# connecting frontend api and backend api 
from flask_cors import CORS

# model layer
from model import UserDao, TweetDao
# service layer
from service import UserService, TweetService
# view layer
from view import create_endpoints

import boto3

class Services :
    pass

################################################
# Create App
################################################

def create_app(test_config = None) :
    app = Flask(__name__)
    
    CORS(app)
    
    if test_config is None :
        app.config.from_pyfile("config.py")
    else :
        app.config.update(test_config)
        
    database = create_engine(app.config['DB_URL'], max_overflow=0)
    
    ##############################################################################################
    ## Persistence Layer : call class and input database engine obj
    ##############################################################################################
    
    user_dao = UserDao(database)
    tweet_dao = TweetDao(database)
    
    ##############################################################################################
    ## Business Layer
    ##############################################################################################
    
    ### create boto3.client() obj for connecting AWS S3
    s3_client = boto3.client("s3",
                             aws_access_key_id = config.S3_ACCESS_KEY,
                             aws_secret_access_key = config.S3_SECRET_KEY)
    
    # s3_client = boto3.client("s3",
    #                          aws_access_key_id = config.test_config['S3_ACCESS_KEY'],
    #                          aws_secret_access_key = config.test_config['S3_SECRET_KEY'])

    services = Services
    ## app.config parameter using for make token : UserService -> generate_access_token -> jwt.encode()
    services.user_service = UserService(user_dao, app.config, s3_client)
    services.tweet_service = TweetService(tweet_dao)
    
    ## endpoint
    create_endpoints(app, services)
    
    ## app is connected 3 layers (persistence, business, presentation)
    return app
    
