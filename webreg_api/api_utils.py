from datetime import datetime
from datetime import timedelta
from flask import jsonify

def build_response(sql_result):
    '''Builds response'''
    if sql_result == None:
        return {'body': 'Requested resource does not exist'}, 404

    for k,v in sql_result.items():
        if type(v) == timedelta:
            sql_result[k] = str(v)
    return {'body': sql_result}, 200
