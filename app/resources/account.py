from flask import request, redirect, render_template, make_response
from flask_restful import Resource, reqparse
from app import app, mongo
from email.message import EmailMessage
import random
import smtplib
from uuid import uuid4

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'support@psty.io',
    "MAIL_PASSWORD": 'nzoyioxgqnanidau'
}

def register_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True)
    return parser

def confirm_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('tfa_code', required=True)
    return parser

class Register(Resource):
    def post(self):
        parser = register_parser()
        args = parser.parse_args()
        email = args['email']
        tfa_code = str(str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
        match = mongo.db.registrations.find_one({ 'email': email })
        if match:
            print('Found')
        auth = (mail_settings['MAIL_USERNAME'], mail_settings['MAIL_PASSWORD'])
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(auth[0], auth[1])
        msg = EmailMessage()
        msg.set_content('Your Authentication Token Is: {}'.format(tfa_code))
        msg['Subject'] = "Your psty.io 2FA Code"
        msg['From'] = "psty.io <support@psty.io>"
        msg['To'] = email
        server.send_message(msg)
        entry_obj = {
            'email': args['email'],
            '2fa': tfa_code
        }
        if not match:
            mongo.db.registrations.insert_one(entry_obj)
        else:
            mongo.db.registrations.find_one_and_replace({'email': str(email)}, entry_obj)
        resp = make_response({'msg': '2FA Sent Successfully'}, 200)
        resp.set_cookie('email', email)
        return resp

class Confirm(Resource):
    def post(self):
        parser = confirm_parser()
        args = parser.parse_args()
        tfa_code = args.get('tfa_code')
        cookies = request.cookies
        if not cookies.get('email'):
            return redirect('https://psty.io/signup', 200)
        email = cookies.get('email')
        register_obj = mongo.db.registrations.find_one({ 'email': email })
        if tfa_code == register_obj['2fa']:
            resp = make_response({'msg': 'Logged In!'}, 200)
            resp.set_cookie('authentication_code', auth_code)
            return resp
        else:
            return { 'error': '2FA Failed!' }, 302
