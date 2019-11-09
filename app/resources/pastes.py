from app import app, mongo
from flask import request, redirect, render_template, send_file, make_response
from flask_restful import Resource, reqparse
from app.resources.helpers import checkPrivate, checkPassword
import jinja2

def paste_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('q', required=True)
    return parser

class Pastes(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        parser = paste_parser()
        data = parser.parse_args()
        q = data['q']
        obj = mongo.db.pastes.find_one({'uid': q})
        if obj:
            return make_response(render_template('index.html', code=jinja2.Markup(obj['code']), raw=str(app.home_url + '/r?q=' + q), lang=str(obj['language'])), 200, headers)
        else:
            return make_response(render_template('404.html'), 404, headers)