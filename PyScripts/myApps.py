from re import template
from flask import render_template, Flask, flash, request, logging, session, redirect, url_for
from flask import Blueprint
from PyScripts.database import *
import os

myAppsBluePrint = Blueprint('myApps', __name__,
                            template_folder='templates')

deleteAppBluePrint = Blueprint('deleteApp', __name__,
                            template_folder='templates')


@myAppsBluePrint.route("/myApps", methods=['GET', 'POST'])
@login_required
def myApps():

    if request.method == "POST":

        pass

    else:

        cursor.execute(
        'SELECT * FROM TBL_Apps WHERE user_id=%s', (session["user_id"],))
        app = cursor.fetchall()

        apps = []

        for i in app:

            cursor.execute(
            'SELECT * FROM TBL_Links WHERE app_id=%s', (i[0],))
            links = cursor.fetchall()

            apps.append([i, links])

        if session["flag"] != 99:

            flag = session["flag"]
            flagText = session["flagText"]

            session["flag"] = 99

            return render_template("/myApps.html", flag=flag, flagText=flagText,apps=apps, myUrl=myUrl)

        else:

            return render_template("/myApps.html", apps=apps, myUrl=myUrl)


@myAppsBluePrint.route("/deleteApp", methods=['GET', 'POST'])
@login_required
def deleteApp():

    if request.method == "POST":

        try:

            appId = request.form['deleteAppInput']
            appName = request.form['appNameInput']

            cursor.execute(
            'SELECT user_id FROM TBL_Apps WHERE app_id=%s and user_id=%s', (appId,session["user_id"],))
            user = cursor.fetchall()[0][0]

            cursor.execute(
            'SELECT link_id FROM TBL_Links WHERE app_id=%s', (appId,))
            links = cursor.fetchall()

            for i in links:

                cursor.execute('DELETE FROM TBL_Links WHERE link_id=%s',(i[0],))
                conn.commit()
            
            cursor.execute('DELETE FROM TBL_Apps WHERE app_id=%s',(appId,))
            conn.commit()
            
            if os.path.exists("static/QrCodes/{}.png".format(appName)):
                os.remove("static/QrCodes/{}.png".format(appName))
            else:
                pass

            session["flag"] = 1
            session["flagText"] = "Your app has been successfully deleted... ({})".format(appName)

            return redirect(url_for("myApps.myApps"))

        except:

            session["flag"] = 2
            session["flagText"] = "Application deletion failed, unexpected error occurred."

            return redirect(url_for("myApps.myApps"))



    else:

        return redirect(url_for("myApps.myApps"))