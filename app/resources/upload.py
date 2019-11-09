from app import app
from app import limiter, rate_limited
from flask import request, redirect, render_template
from flask_restful import Resource, reqparse
from app.resources.constants import languages
from app.resources.helpers import generateOptions
from app import mongo
from uuid import uuid4
import time
import json, jinja2

def upload_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('code', required=True)
    parser.add_argument('lang', required=True)
    return parser

class Upload(Resource):
    def post(self):
        # try:
        parser = upload_parser()
        args = parser.parse_args()
        code = jinja2.escape(args.get('code'))
        raw_code = args.get('code')
        lang = args.get('lang')
        uid = str(uuid4()).split('-')[0][0:5]
        if any(language in lang for language in languages):
            language = lang
        else:
            language = None
        entry_obj = {
            'uid': uid,
            'code': code,
            'raw': raw_code,
            'language': language,
            'uploaded': round(time.time())
        }
        mongo.db.pastes.insert_one(entry_obj)
        return redirect(app.home_url + '/p?q={}'.format(uid), 302)
        # except:
            # return { 'msg': 'Something Broke' }, 500