import psycopg2
from functools import wraps
from flask import session, redirect, url_for, Flask
from flask_recaptcha import ReCaptcha

# Flask app
app = Flask(__name__,template_folder='../templates', static_folder='../static')
app.config['UPLOAD_PATH'] = 'static/uploads'
app.secret_key = b'_softforrange***d*'
app.config['RECAPTCHA_SITE_KEY'] = 'RECAPTCHA_SITE_KEY' # <-- Add your site key
app.config['RECAPTCHA_SECRET_KEY'] = 'RECAPTCHA_SECRET_KEY' # <-- Add your secret key

recaptcha = ReCaptcha(app)

global ServerPort
ServerPort = 5000
global myUrl
myIp = "192.168.1.33"
myUrl = "http://{}:{}/".format(str(myIp), str(ServerPort))

global MyEmail
global MyEmailPass
MyEmail = "your_yandex_mail"
MyEmailPass = "your_password"

# docker-database connect

conn = psycopg2.connect(
    host="db-postgres",
    database="postgres",
    port="5432",
    user="postgres",
    password="123456789Zz.")


"""
conn = psycopg2.connect(
    host="localhost",
    database="teklink",
    port="5432",
    user="postgres",
    password="123456789Zz.")
"""

cursor = conn.cursor()

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "logged_in" in session:
            return f(*args, **kwargs)

        else:

            return redirect(url_for("main"))

    return decorated_function
