from app import app, not_found, mongo
from flask_restful import reqparse, Resource
from flask import request, redirect
from app import limiter
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from app.resources.constants import languages
from uuid import uuid4
from datetime import datetime
import math
import os

def upload_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=FileStorage, location='files')
    return parser


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

class UploadFile(Resource):
    decorators = [limiter.limit("10/second", methods=['POST'])]
    def post(self):
        if 'file' not in request.files:
            print('No Files')
            return redirect('https://psty.io/400.html', 302)
        else:
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save('app/templates/saves/' + filename)
            with open('app/templates/saves/' + filename, 'rb') as f:
                file2 = f.read()
                sz_bytes = len(file2)
                fsize = convert_size(sz_bytes)
                f.close()
            now = datetime.today().strftime('%d-%m-%Y')
            uid = str(uuid4()).split('-')[0]
            uidl = uid[0:4]
            mongo.db.files.insert_one({
                'uid': uidl,
                'filename': str(filename),
                'size': str(fsize),
                'now': now,
                'download_link': 'https://psty.io/d?q={}'.format(filename)
            })
            return redirect('https://psty.io/f?q={}'.format(uidl))