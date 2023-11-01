# file for linking flask to sqlalchemy

from flask import Flask, request, jsonify, current_app, Response, g
from flask_cors import CORS
from sqlalchemy import create_engine, text
#from flask.json import JSONEncoder
import bcrypt
import jwt
import datetime as dt
from functools import wraps


# class CustomJSONEncoder(JSONEncoder) : 
#     def default(self, obj) :
#         if isinstance(obj, set) :
#             return list(obj)
        
#         return JSONEncoder.default(self, obj)

def get_datas(user_follow) :
    user_id_list = []
    follow_id_list = []
    with current_app.database.connect() as con :
        user_ids = con.execute(text(
            """
            SELECT id FROM users ;
            """)).fetchall()
        
        for i in user_ids :
            user_id_list.append(i[0])
            
        follows = con.execute(text(
            """
            SELECT follow_user_id
            FROM users_follow_list
            WHERE user_id = :id ;
            """), {"id": int(user_follow["id"])}).fetchall()
        
        for i in follows :
            follow_id_list.append(i[0])
        
        con.commit()
            
        return user_id_list, follow_id_list
            
def insert_user(new_user) :
    with current_app.database.connect() as con :
        id = con.execute(text(
            """
            INSERT INTO users (name, email, profile, hashed_password)
                        VALUES (:name, :email, :profile, :password) ;
            """), new_user).lastrowid
        
        con.commit()
        
        return id

def get_user(new_user_id) :
    with current_app.database.connect() as con :
        user_info = con.execute(text(
            """
            SELECT id, name, email, profile
            FROM users
            WHERE id = :user_id ;
            """), {"user_id": int(new_user_id)}).fetchone()
        
        return {"id": user_info[0],
                "name": user_info[1],
                "email": user_info[2],
                "profile": user_info[3]} if user_info else "empty"
        
def insert_tweet(user_tweet) :
    with current_app.database.begin() as con :
        row_count = con.execute(text(
            """
            INSERT INTO tweets (user_id, tweet)
                   VALUES (:id, :tweet) ;
            """), user_tweet).rowcount
        
        return row_count
    
def insert_follow(user_follow) :
    with current_app.database.connect() as con :
        row_count = con.execute(text(
            """
            INSERT INTO users_follow_list (user_id, follow_user_id)
                   VALUES (:id, :follow) ;
            """), user_follow).rowcount
        
        con.commit()
        
        return row_count

def insert_unfollow(user_unfollow) :
    with current_app.database.connect() as con :
        row_count = con.execute(text(
            """
            DELETE FROM users_follow_list
            WHERE user_id = :id
            AND follow_user_id = :unfollow ;
            """), user_unfollow).rowcount
        
        con.commit()
        
        return row_count
    
def get_timeline(user_id) :
    with current_app.database.begin() as con :
        rows = con.execute(text(
            """
            SELECT user_id, tweet
            FROM tweets
            WHERE user_id IN (
                SELECT follow_user_id
                FROM users_follow_list
                WHERE user_id = :id)
            OR user_id = :id ;
            """), {"id": user_id}).fetchall()
        
        timeline = [{"user_id": row[0], "tweet": row[1]} for row in rows]
        
        return timeline   
 
def get_user_id_pw(email) :
    with current_app.database.connect() as con :
        row = con.execute(text(
            """
            SELECT id, hashed_password
            FROM users
            WHERE email = :email ;
            """), {'email': email}).fetchone()
        
        con.commit()
        
        return {'id': row[0], 'hashed_password': row[1]} if row else None  
    
##########################################################
# auth decorator function login_required()
# using '/tweet', '/follow', '/unfollow' endpoint
##########################################################    
def login_required(f) :
    @wraps(f)
    def decorated_function(*args, **kwargs) :
        access_token = request.headers.get('Authorization')
        if access_token is not None :
            try :
                payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], 'HS256')
            except jwt.InvalidTokenError:
                payload = None
                
            if payload is None :
                return Response(status=401)
            
            user_id = payload['user_id']
            g.user_id = user_id
            g.user = get_user(user_id) if user_id else None
            
        else :
            return Response(status=401)
        
        return f(*args, **kwargs)
    
    return decorated_function

def create_app(test_config=None) : 
    app = Flask(__name__)
    CORS(app)
    
    if test_config is None :
        app.config.from_pyfile("config.py")
    else :
        app.config.update(test_config)
        
    database = create_engine(app.config["DB_URL"], max_overflow=0)
    app.database = database
    
    # endpoint
    @app.route('/ping', methods=["GET"])
    def ping() :
        return "pong"
       
    @app.route('/sign-up', methods=['POST'])
    def sign_up() : 
        ## HTTP request -> json type : include users info
        new_user = request.json
        ## transfer pw : bcrypt.hashpw
        new_user['password'] = bcrypt.hashpw(new_user['password'].encode('utf-8'), bcrypt.gensalt())
        ## func insert_user : insert into database about new users info
        ## and return new users id (auto create) 
        new_user_id = insert_user(new_user)
        ## func get_user : return users info from database, use new_user_id
        new_user_info = get_user(new_user_id)
        
        return jsonify(new_user_info)
    
    @app.route('/login', methods=['POST'])
    def login() : 
        credential = request.json
        insert_email = credential['email']
        insert_password = credential['password']
        user_credential = get_user_id_pw(insert_email)
        
        ## bcrypt.checkpw(a, b) : True or False
        if user_credential and bcrypt.checkpw(insert_password.encode('UTF-8'), user_credential['hashed_password'].encode('UTF-8')) :
            user_id = user_credential['id']
            payload = {
                'user_id': user_id,
                'exp': dt.datetime.utcnow() + dt.timedelta(seconds = 60 * 60 * 24)
            }
            token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
            
            return jsonify({'access_token': token})
        
        else :
            return '', 401
        
    @app.route('/tweet', methods=['POST'])
    ## login auth decorator
    @login_required
    def tweet() :
        user_tweet = request.json
        user_tweet['id'] = g.user_id
        tweet = user_tweet["tweet"]
        
        if len(tweet) > 300 :
            return "tweet is over 300 latter", 400
        
        insert_tweet(user_tweet)
        
        return '', 200
    
    @app.route('/follow', methods=['POST'])
    ## login auth decorator
    @login_required
    def follow() :
        payload = request.json
        payload['id'] = g.user_id
        
        insert_follow(payload)
        
        # all_ids, follow_ids = get_datas(payload)
        # if int(payload["id"]) not in all_ids or int(payload["follow"]) not in all_ids :
        #     return "error : id or follow id is not in id list", 400
        
        # else :
        #     if int(payload["follow"]) in follow_ids :
        #         return "error : follow id is duplicated", 400
            
        #     else :
        #         insert_follow(payload)
        
        #         return '', 200
        
        return '', 200
    
    @app.route('/unfollow', methods=['POST'])
    ## login auth decorator
    @login_required
    def unfollow() :
        payload = request.json
        payload['id'] = g.user_id
        
        insert_unfollow(payload)
        
        # all_ids, follow_ids = get_datas(payload)
        # if int(payload["id"]) not in all_ids or int(payload["unfollow"]) not in all_ids :
        #     return "error : id or unfollow id is not in id list", 400
        
        # else :
        #     if int(payload["unfollow"]) not in follow_ids :
        #         return "error : unfollow id is not in follow list", 400
            
        #     else :
        #         insert_unfollow(payload)
                
        #         return '', 200
        
        return '', 200
        
    @app.route('/timeline/<int:user_id>', methods=['GET'])
    ## login auth decorator
    @login_required
    def timeline(user_id) :
        user_id = g.user_id
        
        return jsonify({"user_id": user_id, "timeline": get_timeline(user_id)})
        
    @app.route('/view-data2', methods=['GET'])
    def view_data2() :
        payload = request.json
        query = payload['query']
        datas = {}
        with app.database.connect() as con :
            result = con.execute(text(query))
            q = query.split(" ")
            ele_query = [e.replace(",", "") for e in q]
            cols = ele_query[ele_query.index("select")+1 : ele_query.index("from")]
            for i, ele in enumerate(result) :
                k = []
                v = []
                for j in range(len(cols)) :
                    k.append(cols[j])
                    v.append(ele[j]) 
                    datas[i] = dict(zip(k, v))
                
            return jsonify(datas)
        
    return app