from configparser import ConfigParser
import pymysql

def setup_database_connection(config_file):
    '''Sets up the MySQL database connection and returns the connection'''
    config = ConfigParser()
    config.read(config_file)
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
