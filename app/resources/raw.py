from app import app as app
from flask import request, redirect, render_template, send_file, make_response
from flask_restful import Resource, reqparse
from app import mongo

def paste_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('q', required=True)
    return parser

class Raw(Resource):
    def get(self):
        headers = {'Content-Type': 'text/plain'}
        try:
            parser = paste_parser()
            data = parser.parse_args()
            obj = mongo.db.pastes.find_one({'uid': data['q']})
            raw = obj['raw']
            return make_response(raw, 200, headers)
        except:
            return make_response(render_template('404.html'), 404, headers)
