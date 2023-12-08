# app config
db = {
    "user": "root",
    "password": "hshkuber1234",
    "host": "localhost",
    "port": 3306,
    "database": "minitter"
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
JWT_SECRET_KEY = "adminadmin1234"
JWT_EXP_DELTA_SECONDS = 7 * 24 * 60 * 60

# file save path
UPLOAD_DIRECTORY = "./profile_pictures"

# AWS S3
S3_BUCKET = 'minitterbucket'
S3_ACCESS_KEY = 'AKIA2ARTLA6KYVL7L3GF'
S3_SECRET_KEY = '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'
# add region code 
S3_BUCKET_URL = f"http://{S3_BUCKET}.s3.ap-northeast-2.amazonaws.com/" 

# unit test config
test_db = {
    "user": "root",
    "password": "hshkuber1234",
    "host": "localhost",
    "port": 3306,
    "database": "test_db"
}

test_config = {
    'DB_URL': f"mysql+mysqlconnector://{test_db['user']}:{test_db['password']}@{test_db['host']}:{test_db['port']}/{test_db['database']}?charset=utf8",
    'JWT_SECRET_KEY' : "adminadmin1234",
    'JWT_EXP_DELTA_SECONDS': 7 * 24 * 60 * 60,
    'S3_BUCKET': "test",
    'S3_ACCESS_KEY': "test_access_key",
    'S3_SECRET_KEY': "test_secret_key",
    'S3_BUCKET_URL': f"https://s3.ap-northeast-2.amazonaws.com/test/"
}




