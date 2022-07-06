import psycopg2
from functools import wraps
from flask import session, redirect, url_for

global ServerIp
global ServerPort

ServerIp = "0.0.0.0"
ServerPort = 5000

global myUrl
myIp = "your_public_ip"
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