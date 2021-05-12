from configparser import ConfigParser
import pymysql
import os

def setup_database_connection():
    '''Sets up the MySQL database connection and returns the connection'''
    is_prod = os.getenv('IS_HEROKU')
    host = None
    user = None
    password = None
    db = None

    if is_prod:
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASS')
        db = os.getenv('DB_DB')
    else:
        config = ConfigParser()
        config.read('config.ini')
        host = config['database']['host']
        user = config['database']['user']
        password = config['database']['password']
        db = config['database']['db']

    connection = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

def build_table_name(year, quarter):
    return f'{year}_{quarter}_courses'
