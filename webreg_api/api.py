from flask import Flask
from flask_restful import Resource, Api, reqparse
# from webreg_api import database, api_utils
import database, api_utils
import pymysql
from datetime import datetime

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('code')
parser.add_argument('year')
parser.add_argument('quarter')

# Database setup
config_file = '../config.ini'
connection = database.setup_database_connection(config_file)
cursor = connection.cursor()

# Course
# Returns course info of the given course code
class Course(Resource):
    def get(self):
        return {'body': 'Welcome to Course Routes'}

    def post(self):
        try:
            args = parser.parse_args()
            code = int(args['code'])
            year = args['year']
            quarter = args['quarter']
            table_name = database.build_table_name(year, quarter)
            query = f'SELECT * FROM {table_name} WHERE code=%s'
            cursor.execute(query, [code])
            sql_result = cursor.fetchone()
            response = api_utils.build_response(sql_result)
            return response
        except:
            return {'body': 'Error in request'}, 500

# API Routes
api.add_resource(Course, '/')

if __name__ == '__main__':
    app.run(debug=True)
