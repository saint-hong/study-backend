# sqlalchemy test file
## database connect information

db = {
    "user": "root",
    "password": "hshkuber1234",
    "host": "localhost",
    "port": 3306,
    "database": "minitter"
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
JWT_SECRET_KEY = 'adminadmin1234'
