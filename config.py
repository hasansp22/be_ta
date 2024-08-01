import os

# CORS_HEADERS = 'application/json'
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HOST = str(os.environ.get("DB_HOST"))
    DATABASE = str(os.environ.get("DB_DATABASE"))
    USERNAME = str(os.environ.get("DB_USERNAME"))
    PASSWORD = str(os.environ.get("DB_PASSWORD"))

    SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    # JWT_TOKEN_LOCATION = str(os.environ.get('headers', 'query_string'))
    # JWT_QUERY_STRING_NAME = str(os.environ.get('jwt'))
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DATABASE
    SQLACHEMY_TRACK_MODIFICATIONS = False
    SQLACHEMY_RECORD_QUERIES = True
    