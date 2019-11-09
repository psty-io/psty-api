from flask import Flask, request, redirect, render_template, send_file
from flask_restful import Resource, Api
from flask_limiter import Limiter, util
from flask_pymongo import PyMongo
from app.resources.constants import languages, themes
from app.resources.helpers import generateOptions
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz, os, json, atexit, time

app = Flask(__name__)
api = Api(app)

app.config['MONGO_URI'] = ''
# app.home_url = 'http://localhost:5000'

mongo = PyMongo(app)

def drop_pastes():
    print('Finding Pastes')
    now = time.time()
    collection = mongo.db.pastes
    for document in collection.find():
        if document.get('uploaded'):
            print('Found One')
            remainder = int(now - document.get('uploaded'))
            if remainder >= 86400:
                mongo.db.pastes.delete_one(document)
            else:
                print('Not 24 Hours Old')
                pass

scheduler = BackgroundScheduler()
scheduler.add_job(func=drop_pastes, trigger="interval", seconds=120)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

@app.errorhandler(429)
def rate_limited(e):
    return render_template('429.html')

@app.errorhandler(500)
def server_main(e):
    return render_template('500.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('400.html')

limiter = Limiter(
    app,
    key_func=util.get_remote_address,
    default_limits=["200000 per day", "50000 per hour"]
)

app.home_url = 'https://psty.io'

@app.route('/')
def returnit():
    return redirect(app.home_url + '/new')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/mobile')
def mobile():
    options = generateOptions(languages)
    
    return render_template('mobile.html', options=options)


@app.route('/new')
def get():
    options = generateOptions(languages)
    themesl = generateOptions(themes)
    count = 1000
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
    
    return render_template('new.html', options=options, count=count, remaining=remaining, themes=themesl)

@app.route('/assets/css/<css>')
def css(css):
    return send_file('templates/assets/css/{}'.format(css))

@app.route('/assets/sass/<path>')
def sass(path):
    return send_file('templates/assets/sass/{}'.format(path))

@app.route('/assets/js/<js>')
def js(js):
    return send_file('templates/assets/js/{}'.format(js))

@app.route('/assets/images/<image>')
def image(image):
    return send_file('templates/assets/images/{}'.format(image))

@app.route('/files')
def files():
    return render_template('file_upload.html')

@app.route('/about')
def about():
    return render_template('about.html')

from app.resources import upload
from app.resources import pastes
from app.resources import openapi
from app.resources import raw
from app.resources import file
from app.resources import download
from app.resources import upload_file
from app.resources import account

api.add_resource(upload.Upload, '/upload')
api.add_resource(pastes.Pastes, '/p')
api.add_resource(openapi.OpenApi, '/api')
api.add_resource(raw.Raw, '/r')
api.add_resource(file.File, '/f')
api.add_resource(upload_file.UploadFile, '/upload_file')
api.add_resource(download.Download, '/d')
api.add_resource(account.Register, '/signup')