from app import app, mongo
from flask_restful import reqparse, Resource
from flask import request
from app import limiter
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from app.resources.constants import languages
from uuid import uuid4
import jinja2

def upload_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('code', required=True)
    parser.add_argument('lang', required=True)
    parser.add_argument('theme')
    return parser

class OpenApi(Resource):
    def post(self):
        try:
            parser = upload_parser()
            args = parser.parse_args()
            code = jinja2.escape(args.get('code'))
            raw_code = args.get('code')
            lang = args.get('lang')
            theme = args.get('theme')
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
                'theme': theme
            }
            mongo.db.pastes.insert_one(entry_obj)
            return {
                'status': 200,
                'message': 'Paste Successful',
                'paste_link': 'https://psty.io/p?q={}'.format(uid),
                'raw_link': 'https://psty.io/r?q={}'.format(uid)
            }, 200
        except Exception as e:
            return {
                'status': 500,
                'error': 'Something went wrong. Message = Exception',
                'message': e
            }