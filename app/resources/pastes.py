from app import app
from flask import request, redirect, render_template, send_file, make_response
from flask_restful import Resource, reqparse

def paste_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('q', required=True)
    return parser

class Pastes(Resource):
    def get(self):
        parser = paste_parser()
        data = parser.parse_args()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('pastes/{}'.format(data['q'])), 200, headers)
