from app import app
from flask import request, redirect, render_template, send_file, make_response
from flask_restful import Resource, reqparse
from app.resources.helpers import checkPrivate, checkPassword

def paste_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('q', required=True)
    return parser

class Download(Resource):
    def get(self):
        parser = paste_parser()
        data = parser.parse_args()
        if '../' in data['q'] or '..' in data['q']:
            return { 'bitch': 'foh with your path traversal headass bitch asss' }, 200
        filename = data['q']
        return send_file('templates/saves/{}'.format(filename), as_attachment=True)
