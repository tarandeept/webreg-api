from flask import Flask
from flask_restful import Resource, Api
import pymysql
from webreg_api import database, api_utils
# import database, api_utils

app = Flask(__name__)
api = Api(app)

# Database setup
connection = database.setup_database_connection()
cursor = connection.cursor()

# Hello
class Hello(Resource):
    def get(self):
        return {'message': 'Hello world'}

# Course
# Returns course info of the given course code
class Course(Resource):
    def get(self, code, year, quarter):
        table_name = database.build_table_name(year, quarter)
        query = f'SELECT * FROM {table_name} WHERE code=%s'
        cursor.execute(query, [code])
        sql_result = cursor.fetchone()
        response = api_utils.build_response(sql_result)
        return response

# Department
# Returns all courses within the given department
class Department(Resource):
    def get(self, dept, year, quarter):
        table_name = database.build_table_name(year, quarter)
        query = f'SELECT * FROM {table_name} WHERE dept=%s'
        cursor.execute(query, [dept])
        sql_result = cursor.fetchall()
        response = api_utils.build_response(sql_result)
        return response

# API Routes
api.add_resource(Hello, '/')
api.add_resource(Course, '/api/course/<int:code>/<int:year>/<string:quarter>')
api.add_resource(Department, '/api/dept/<string:dept>/<int:year>/<string:quarter>')

if __name__ == '__main__':
    app.run(debug=True)
    connection.close()
