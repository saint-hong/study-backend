# view layer code : endpoint of source code
from flask  import request, jsonify, current_app, Response, g, send_file
from flask.json import JSONEncoder
from functools import wraps
from werkzeug.utils import secure_filename
import jwt

# transform data type if using set data type
class CustomJSONEncoder(JSONEncoder) :
    def dafault(self, obj) : 
        if isinstance(obj, set) : 
            return list(obj)
        return JSONEncoder.default(self, obj)

################################################################
#     Decorators
################################################################

# check the access_token
def login_required(f) : 
    @wraps(f)
    def decorated_function(*args, **kwargs) : 
        access_token = request.headers.get('Authorization')
        if access_token is not None :
            try :
                payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], 'HS256')
            except jwt.InvalidTokenError :
                payload = None
            if payload is None :
                return Response(status=401)
            
            ## user_id in decoded access_token ---> saved g.user_id
            user_id = payload['user_id']
            g.user_id = user_id
            
        else :
            return Response(status=401)
        
        return f(*args, **kwargs)
    return decorated_function

# end points here
def create_endpoints(app, services) : 
    app.json_encoder = CustomJSONEncoder
    user_service = services.user_service
    tweet_service = services.tweet_service
    
    @app.route('/ping', methods=['GET'])
    def ping() :
        return 'some some pong'
    
    @app.route('/view-data', methods=['GET'])
    def view_data() :
        payload = request.json
        user_id = payload['id']
        datas = user_service.get_user(user_id)
        
        return datas
    
    @app.route('/sign-up', methods=['POST'])
    def sign_up() :
        new_user = request.json
        new_user_id = user_service.create_new_user(new_user)
        new_user_info = user_service.get_user(new_user_id)
        
        return jsonify(new_user_info)
    
    @app.route('/login', methods=['POST'])
    def login() :
        payload = request.json
        authorized, id = user_service.login(payload)
        
        if authorized :
            #user_credential = user_service.get_user_id_and_password(payload['email'])
            user_id = int(id)
            token = user_service.generate_access_token(user_id)
            
            return jsonify({'user_id': user_id, 
                            'access_token': token})
        else :
            return '', 401
        
    @app.route('/follow', methods=['POST'])
    @login_required
    def follow() :
        payload = request.json
        user_id = g.user_id
        follow_id = payload['follow']
        
        user_service.follow(user_id, follow_id)
        
        return '', 200
    
    @app.route('/unfollow', methods=['POST'])
    @login_required
    def unfollow() : 
        payload = request.json
        user_id = g.user_id
        unfollow_id = payload['unfollow']
        
        user_service.unfollow(user_id, unfollow_id)
        
        return '', 200
    
    @app.route('/tweet', methods=['POST'])
    @login_required
    def tweet() :
        user_tweet = request.json
        user_tweet['id'] = g.user_id
        #tweet = user_tweet['tweet']
        
        result = tweet_service.tweet(user_tweet)
        if result is None :
            return 'over 300 character', 400
        
        return '', 200
    
    @app.route('/timeline', methods=['GET'])
    @login_required
    def timeline() :
        user_id = g.user_id
        timeline = tweet_service.timeline(user_id)
        
        return jsonify({'user_id': user_id, 'timeline': timeline})
    
    ## upload picture endpoint
    @app.route('/profile-picture/<string:location>', methods=['POST'])
    @login_required
    def upload_profile_picture(location) :
        
        user_id = g.user_id
        
        ## "profile-pic" is non pix name of form which request body content-type
        if 'profile-pic' not in request.files :
            return 'File is missing', 404
        
        profile_pic = request.files['profile-pic']
        
        if profile_pic.filename == '' :
            return 'File is missing', 404
        
        filename = secure_filename(profile_pic.filename)
        
        if location == 'local' :
            user_service.save_profile_picture_local(profile_pic, filename, user_id)
        
        elif location == 's3' : 
            user_service.save_profile_picture_s3(profile_pic, filename, user_id)
        
        return '', 200
    
    ## download picture endpoint
    ## download free pic : not use @login_required
    @app.route('/profile-picture/<string:location>/<int:user_id>', methods=['GET'])
    def get_profile_picture(location, user_id) :
        
        profile_picture = user_service.get_profile_picture_local(user_id)
        
        if location == 'local' :    
            if profile_picture :
                return send_file(profile_picture), 200
            else :
                return '', 404
        ## transform s3 url addr to json type
        elif location == 's3' : 
            if profile_picture : 
                return jsonify({'img_url': profile_picture})
            else :
                return '', 404