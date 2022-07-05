from flask import render_template, session, redirect, url_for, request
from flask import Blueprint
from PyScripts.tools import *
import os
import qrcode

myAppsBluePrint = Blueprint('myApps', __name__,
                            template_folder='templates')

deleteAppBluePrint = Blueprint('deleteApp', __name__,
                               template_folder='templates')


@myAppsBluePrint.route("/myApps", methods=['GET', 'POST'])
@login_required
def myApps():

    if request.method == "POST":

        try:

            appId = request.form['updateAppInput']
            appNameInput = request.form['appNameInput']

            cursor.execute(
                'SELECT user_id FROM TBL_Apps WHERE app_id=%s and user_id=%s', (appId, session["user_id"],))
            user = cursor.fetchall()[0][0]

        except:

            session["flag"]=2
            session["flagText"]="System Error, changes could not be saved"

            return redirect(url_for("myApps.myApps"))


        appName = request.form['appName']

        if appName.isalnum()==False:

            session["flag"]=2
            session["flagText"]="Your application name must not contain non-alphanumeric characters."

            return redirect(url_for("myApps.myApps"))

        notSTR="\"!'^+%&/()=?_-*\\,><;:.é£#$½¾\{\}[] "

        for i in notSTR:

            if str(i) in str(appName):

                session["flag"]=2
                session["flagText"]="Your application name must not contain \"{}\" character.".format(i)

                return redirect(url_for("myApps.myApps"))


        if len(str(appName)) > 3 and len(str(appName)) < 30:

            try:

                if appNameInput!=appName:

                    cursor.execute('SELECT app_id FROM TBL_Apps WHERE lower(app_name)=%s',(appName.lower(),))
                    App_id = cursor.fetchall()
                    App_id = App_id[0][0]

                    if App_id!=None or len(App_id)!=0:

                        session["flag"]=2
                        session["flagText"]="This app name is being used by someone else, please try another app name."

                        return redirect(url_for("myApps.myApps"))

            except:

                if appNameInput!=appName:

                    cursor.execute('UPDATE TBL_Apps SET app_name=%s WHERE app_id=%s and user_id=%s',
                    (appName, appId, session["user_id"],))
                    conn.commit()

                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_H,
                        box_size=10,
                        border=3,
                    )

                    qr.add_data('{}{}'.format(myUrl,appName))
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

                    img.save("static/QrCodes/{}.png".format(appName))
                    
                    if os.path.exists("static/QrCodes/{}.png".format(appNameInput)):
                        os.remove("static/QrCodes/{}.png".format(appNameInput))
                    else:
                        pass

            linkCount = 0

            try:	

                apple = request.form['iosText']

                if len(apple) < 3 or len(apple) >130 :

                    session["flag"]=2
                    session["flagText"]="The link length must be between 3 and 130 characters."

                    return redirect(url_for("myApps.myApps"))

                flaga = "http://" in apple
                flagb = "https://" in apple

                if flaga!=True and flagb!=True:

                    session["flag"]=2
                    session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

                    return redirect(url_for("myApps.myApps"))
				
                linkCount+=1

            except:
			
                pass

            try:

                android = request.form['androidText']

                if len(android) < 3 or len(android) >130 :
					
                    session["flag"]=2
                    session["flagText"]="The link length must be between 3 and 130 characters."

                    return redirect(url_for("myApps.myApps"))

                flaga = "http://" in android
                flagb = "https://" in android

                if flaga!=True and flagb!=True:

                    session["flag"]=2
                    session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

                    return redirect(url_for("myApps.myApps"))

                linkCount+=1

            except:

                pass

            try:

                huawei = request.form['huaweiText']

                if len(huawei) < 3 or len(huawei) >130 :
					
                    session["flag"]=2
                    session["flagText"]="The link length must be between 3 and 130 characters."

                    return redirect(url_for("myApps.myApps"))


                flaga = "http://" in huawei
                flagb = "https://" in huawei

                if flaga!=True and flagb!=True:

                    session["flag"]=2
                    session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

                    return redirect(url_for("myApps.myApps"))

                linkCount+=1

            except:

                pass

            try:

                windows = request.form['windowsText']

                if len(windows) < 3 or len(windows) >130 :
					
                    session["flag"]=2
                    session["flagText"]="The link length must be between 3 and 130 characters."

                    return redirect(url_for("myApps.myApps"))


                flaga = "http://" in windows
                flagb = "https://" in windows

                if flaga!=True and flagb!=True:

                    session["flag"]=2
                    session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

                    return redirect(url_for("myApps.myApps"))

                linkCount+=1

            except:

                pass


            try:

                ubuntu = request.form['ubuntuText']

                if len(ubuntu) < 3 or len(ubuntu) >130 :
					
                    session["flag"]=2
                    session["flagText"]="The link length must be between 3 and 130 characters."

                    return redirect(url_for("myApps.myApps"))

                flaga = "http://" in ubuntu
                flagb = "https://" in ubuntu

                if flaga!=True and flagb!=True:

                    session["flag"]=2
                    session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

                    return redirect(url_for("myApps.myApps"))

                linkCount+=1

            except:

                pass

            if linkCount==0:

                session["flag"]=2
                session["flagText"]="Please add at least one link to the application."

                return redirect(url_for("myApps.myApps"))

            App_id = request.form['updateAppInput']

            try:
				
                try:
                    apple=str(apple)
                except:

                    apple = "-"

                cursor.execute('UPDATE TBL_Links SET link_url=%s WHERE app_id=%s and link_name=%s',
                (apple, App_id, "Apple",))
                conn.commit()

            except:

                pass

            try:

                try:
                    android=str(android)
                except:

                    android = "-"

                cursor.execute('UPDATE TBL_Links SET link_url=%s WHERE app_id=%s and link_name=%s',
                (android, App_id, "Android",))
                conn.commit()

            except:

                pass

            try:

                try:
                    huawei=str(huawei)
                except:

                    huawei = "-"

                cursor.execute('UPDATE TBL_Links SET link_url=%s WHERE app_id=%s and link_name=%s',
                (huawei, App_id, "Huawei",))
                conn.commit()

            except:

                pass

            try:

                try:
                    windows=str(windows)
                except:

                    windows = "-"

                cursor.execute('UPDATE TBL_Links SET link_url=%s WHERE app_id=%s and link_name=%s',
                (windows, App_id, "Windows", ))
                conn.commit()

            except:

                pass

            try:

                try:
                    ubuntu=str(ubuntu)
                except:

                    ubuntu = "-"

                cursor.execute('UPDATE TBL_Links SET link_url=%s WHERE app_id=%s and link_name=%s',
                (ubuntu, App_id, "Ubuntu", ))
                conn.commit()

            except:
                pass

                
            
            session["flag"]=0
            session["flagText"]="Application update process successful."

            return redirect(url_for("myApps.myApps"))


        else:

            session["flag"]=2
            session["flagText"]="The application name must be between 3 and 30 characters."

            return redirect(url_for("myApps.myApps"))

    else:

        cursor.execute(
            'SELECT * FROM TBL_Apps WHERE user_id=%s ORDER BY app_id', (session["user_id"],))
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

            return render_template("/myApps.html", flag=flag, flagText=flagText, apps=apps, myUrl=myUrl)

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
                'SELECT user_id FROM TBL_Apps WHERE app_id=%s and user_id=%s', (appId, session["user_id"],))
            user = cursor.fetchall()[0][0]


            cursor.execute(
            'DELETE FROM TBL_Links WHERE app_id=%s', (appId,))
            conn.commit()


            cursor.execute('DELETE FROM TBL_Apps WHERE app_id=%s', (appId,))
            conn.commit()

            if os.path.exists("static/QrCodes/{}.png".format(appName)):
                os.remove("static/QrCodes/{}.png".format(appName))
            else:
                pass

            cursor.execute('UPDATE TBL_Users SET user_appcount=user_appcount-1 WHERE user_id=%s',
			(session["user_id"],))
            conn.commit()

            session["flag"] = 1
            session["flagText"] = "Your app has been successfully deleted... ({})".format(appName)

            return redirect(url_for("myApps.myApps"))

        except:

            session["flag"] = 2
            session["flagText"] = "Application deletion failed, unexpected error occurred."

            return redirect(url_for("myApps.myApps"))

    else:

        return redirect(url_for("myApps.myApps"))
