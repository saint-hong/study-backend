# business layer about logic of users service : create user data, follow, unfollow
from datetime import datetime, timedelta
import jwt
import bcrypt
import os



class UserService :
    
    def __init__(self, user_dao, config, s3_client) : 
        ## data base of persistance layer
        ## dao : Data Access Object 
        self.user_dao = user_dao
        self.config = config
        ## import boto3.client() from app.py
        self.s3 = s3_client
        
        # self.s3 = boto3.client('s3', 
        #                        aws_access_key_id = config['S3_ACCESS_KEY'], 
        #                        aws_secret_access_key = config['S3_SECRET_KEY'])
        
    def create_new_user(self, new_user) :
        ## new_user is parameter of presentation layer '/sign-up' endpoint 
        new_user['password'] = bcrypt.hashpw(new_user['password'].encode('UTF-8'), bcrypt.gensalt())
        new_user_id = self.user_dao.insert_user(new_user)
        
        return new_user_id
    
    def get_user(self, new_user_id) : 
        new_user_data = self.user_dao.get_user_data(new_user_id)
        
        return new_user_data
    
    def login(self, credential) :
        ## credential is parameter of presentation layer '/login' endpoint
        email = credential['email']
        password = credential['password']
        ## get id, pw from db
        user_credential = self.user_dao.get_user_id_and_password(email)
        user_id = user_credential['id']
        ## T and T = T, T and F = F
        authorized = user_credential and bcrypt.checkpw(password.encode('UTF-8'), user_credential['hashed_password'].encode('UTF-8'))
        
        return authorized, user_id
        
    def generate_access_token(self, user_id) : 
        ## user_id is parameter of presentation layer '/login' endpoint
        payload = {'user_id': user_id,
                   'exp': datetime.utcnow() + timedelta(seconds=60*60*24)}
        token = jwt.encode(payload, self.config['JWT_SECRET_KEY'], 'HS256')
        
        return token
    
    def follow(self, user_id, follow_id) : 
        ## user_id, follow_id is parameter of presentation layer '/follow' endpoint
        ## call db and update follow id data (insert follow id)
        return self.user_dao.insert_follow(user_id, follow_id)
    
    def unfollow(self, user_id, unfollow_id) : 
        ## user_id, unfollow_id is parameter of presentation layer '/unfollow' endpoint
        ## call db and update unfollow id data (delete follow id)
        return self.user_dao.insert_unfollow(user_id, unfollow_id)
    
    # call by view layers endpoint : POST /profile-picture
    def save_profile_picture_local(self, picture, filename, user_id) :
        
        ## make path for save
        profile_pic_path_and_name = os.path.join(self.config['UPLOAD_DIRECTORY'], filename)
        picture.save(profile_pic_path_and_name)
        
        ## call user_dao for insert pic in database
        return self.user_dao.save_profile_picture(profile_pic_path_and_name, user_id)
    
    def save_profile_picture_s3(self, picture, filename, user_id) : 
        
        ## upload file to s3 bucket
        self.s3.upload_fileobj(picture, self.config['S3_BUCKET'], filename)
        ## uploaded img url on s3 bucket
        image_url = f"{self.config['S3_BUCKET_URL']}{filename}"
        
        return self.user_dao.save_profile_picture(image_url, user_id)
    
    # call by view layers endpoint : GET /profile-picture
    def get_profile_picture_local(self, user_id) :
        
        return self.user_dao.get_profile_picture(user_id)
    
