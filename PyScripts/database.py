import psycopg2
import socket
from functools import wraps
from flask import session, redirect, url_for

global myUrl
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
myIp = s.getsockname()[0]

myUrl = "http://{}:5600/".format(str(myIp))

conn = psycopg2.connect(
    host="localhost",
    database="teklink",
    port="5432",
    user="postgres",
    password="123456789Zz.")

cursor = conn.cursor()

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "logged_in" in session:
            return f(*args, **kwargs)

        else:

            return redirect(url_for("main"))

    return decorated_function