from flask import Flask
from flask_restful import Resource, Api, reqparse
import database
import pymysql

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

def build_table_name(year, quarter):
    return f'{year}_{quarter}_courses'

# Course
# Returns the Course object of the given course code
class Course(Resource):
    def get(self):
        return {'Home': 'route'}

    def post(self):
        args = parser.parse_args()
        code = int(args['code'])
        year = args['year']
        quarter = args['quarter']
        table_name = build_table_name(year, quarter)
        query = f'SELECT * FROM {table_name} WHERE code=%s'
        cursor.execute(query, [code])
        result = cursor.fetchone()
        print(result)
        return {'place': result['place']}

api.add_resource(Course, '/')

if __name__ == '__main__':
    app.run(debug=True)
