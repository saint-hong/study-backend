# sqlalchemy test file
## database connect information

rds_endpoint = "backend-test-1.c1mer0obgfjg.ap-northeast-2.rds.amazonaws.com"
db = {
    "user": "root",
    "password": "hshkuber1234",
    "host": rds_endpoint,
    "port": 3306,
    "database": "minitter"
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
JWT_SECRET_KEY = 'adminadmin1234'
