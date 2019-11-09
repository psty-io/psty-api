from email.message import EmailMessage
import smtplib

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'support@psty.io',
    "MAIL_PASSWORD": 'nzoyioxgqnanidau'
}

def send_password(email, tfa_code):
    try:
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
        return True
    except:
        return False