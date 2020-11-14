from datetime import datetime
from flask import jsonify

def build_response(sql_result):
    '''Builds response'''
    if sql_result == None:
        return {'body': 'Requested resource does not exist'}, 201

    for k,v in sql_result.items():
        if type(v) == datetime:
            sql_result[k] = v.isoformat()
    return {'body': sql_result}
