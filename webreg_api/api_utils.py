from datetime import datetime
from datetime import timedelta
from flask import jsonify

def build_response(sql_result):
    '''Builds response'''
    if sql_result == None:
        return {'message': 'Requested resource does not exist'}, 404
    return {'data': sql_result}, 200
