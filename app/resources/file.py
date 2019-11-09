from app import app, mongo
from flask import request, redirect, render_template, send_file, make_response
from flask_restful import Resource, reqparse
from app.resources.helpers import checkPrivate, checkPassword
from datetime import datetime
import pytz

def paste_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('q', required=True)
    return parser

class File(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        try:
            parser = paste_parser()
            data = parser.parse_args()
            filename = data['q']
            tz = pytz.timezone('America/New_York')
            hour = datetime.now(tz).strftime('%H')
            minute = datetime.now(tz).strftime('%M')
            til_hour = 23 - int(hour)
            til_minute = 60 - int(minute)
            if til_hour <= 1:
                hours = "1 hour, and"
            else:
                hours = "%s hours, and" % str(til_hour)
            if til_minute == 1:
                minutes = " 1 minute"
            else:
                minutes = " %s minutes" % str(til_minute)
            remaining = hours + minutes
            file_obj = mongo.db.files.find_one({
                'uid': data['q']
            })
            print(file_obj)
            if file_obj:
                return make_response(render_template('download.html', filename=file_obj['filename'], size=file_obj['size'], download=file_obj['download_link'], now=file_obj['now']), 200, headers)
            else:
                return make_response(render_template('404.html'), 404, headers)
        except:
            return make_response(render_template('404.html'), 404, headers)