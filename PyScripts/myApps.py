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

            if session["language"]==0:

                session["flagText"]="System Error, changes could not be saved."

            else:
                session["flagText"]="Sistem Hatası, değişiklikler kaydedilemedi."

            return redirect(url_for("myApps.myApps"))


        appName = request.form['appName']

        blackList = ["login", "register", "home", "replacePass", "myApps", "create", "generate", "me", "tr", "en", "confirm", "resetPass", "logout","demir", "demirai", "sfr", "softforrange"]

        for i in blackList:

            if appName.lower()==i.lower():

                session["flag"]=2

                if session["language"]==0:

                    session["flagText"]="You can't get this app name."

                else:
                    session["flagText"]="Bu uygulama adını alamazsınız."

                return redirect(url_for("myApps.myApps"))

        if appName.isalnum()==False:

            session["flag"]=2

            if session["language"]==0:

                session["flagText"]="Your application name must not contain non-alphanumeric characters."

            else:
                session["flagText"]="Uygulama adınız alfanumerik olmayan karakterler içermemelidir."

            return redirect(url_for("myApps.myApps"))

        notSTR="\"!'^+%&/()=?_-*\\,><;:.é£#$½¾\{\}[] "

        for i in notSTR:

            if str(i) in str(appName):

                session["flag"]=2
                
                if session["language"]==0:

                    session["flagText"]="Your application name must not contain \"{}\" character.".format(i)

                else:
                    session["flagText"]="Uygulama adınız \"{}\" karakterini içermemelidir.".format(i)

                return redirect(url_for("myApps.myApps"))


        if len(str(appName)) > 3 and len(str(appName)) < 30:

            createQR = False

            try:

                if appNameInput!=appName:

                    cursor.execute('SELECT app_id FROM TBL_Apps WHERE lower(app_name)=%s',(appName.lower(),))
                    App_id = cursor.fetchall()
                    App_id = App_id[0][0]

                    if App_id!=None or len(App_id)!=0:

                        session["flag"]=2
                        
                        if session["language"]==0:

                            session["flagText"]="This app name is being used by someone else, please try another app name."

                        else:
                            session["flagText"]="Bu uygulama adı başka biri tarafından kullanılıyor, lütfen başka bir uygulama adı deneyin."

                        return redirect(url_for("myApps.myApps"))

            except:

                createQR=True

            linkCount = 0

            try:	

                apple = request.form['iosText']

                if len(apple) < 3 or len(apple) >130 :

                    session["flag"]=2

                    if session["language"]==0:

                        session["flagText"]="The link length must be between 3 and 130 characters."

                    else:
                        session["flagText"]="Bağlantı uzunluğu 3 ile 130 karakter arasında olmalıdır."

                    return redirect(url_for("myApps.myApps"))

                flaga = "http://" in apple
                flagb = "https://" in apple

                if flaga!=True and flagb!=True:

                    session["flag"]=2
                    if session["language"]==0:

                        session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

                    else:
                        session["flagText"]="Lütfen bağlantılarınızda http:// veya https:// protokollerinden birini belirtin."

                    return redirect(url_for("myApps.myApps"))
				
                linkCount+=1

            except:
			
                pass

            try:

                android = request.form['androidText']

                if len(android) < 3 or len(android) >130 :
					
                    session["flag"]=2
                    
                    if session["language"]==0:

                        session["flagText"]="The link length must be between 3 and 130 characters."

                    else:
                        session["flagText"]="Bağlantı uzunluğu 3 ile 130 karakter arasında olmalıdır."

                    return redirect(url_for("myApps.myApps"))

                flaga = "http://" in android
                flagb = "https://" in android

                if flaga!=True and flagb!=True:

                    session["flag"]=2
                    
                    if session["language"]==0:

                        session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

                    else:
                        session["flagText"]="Lütfen bağlantılarınızda http:// veya https:// protokollerinden birini belirtin."

                    return redirect(url_for("myApps.myApps"))

                linkCount+=1

            except:

                pass

            try:

                huawei = request.form['huaweiText']

                if len(huawei) < 3 or len(huawei) >130 :
					
                    session["flag"]=2

                    if session["language"]==0:

                        session["flagText"]="The link length must be between 3 and 130 characters."

                    else:
                        session["flagText"]="Bağlantı uzunluğu 3 ile 130 karakter arasında olmalıdır."

                    return redirect(url_for("myApps.myApps"))


                flaga = "http://" in huawei
                flagb = "https://" in huawei

                if flaga!=True and flagb!=True:

                    session["flag"]=2

                    if session["language"]==0:

                        session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

                    else:
                        session["flagText"]="Lütfen bağlantılarınızda http:// veya https:// protokollerinden birini belirtin."

                    return redirect(url_for("myApps.myApps"))

                linkCount+=1

            except:

                pass

            try:

                windows = request.form['windowsText']

                if len(windows) < 3 or len(windows) >130 :
					
                    session["flag"]=2

                    if session["language"]==0:

                        session["flagText"]="The link length must be between 3 and 130 characters."

                    else:
                        session["flagText"]="Bağlantı uzunluğu 3 ile 130 karakter arasında olmalıdır."

                    return redirect(url_for("myApps.myApps"))


                flaga = "http://" in windows
                flagb = "https://" in windows

                if flaga!=True and flagb!=True:

                    session["flag"]=2

                    if session["language"]==0:

                        session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

                    else:
                        session["flagText"]="Lütfen bağlantılarınızda http:// veya https:// protokollerinden birini belirtin."

                    return redirect(url_for("myApps.myApps"))

                linkCount+=1

            except:

                pass


            try:

                ubuntu = request.form['ubuntuText']

                if len(ubuntu) < 3 or len(ubuntu) >130 :
					
                    session["flag"]=2

                    if session["language"]==0:

                        session["flagText"]="The link length must be between 3 and 130 characters."

                    else:
                        session["flagText"]="Bağlantı uzunluğu 3 ile 130 karakter arasında olmalıdır."

                    return redirect(url_for("myApps.myApps"))

                flaga = "http://" in ubuntu
                flagb = "https://" in ubuntu

                if flaga!=True and flagb!=True:

                    session["flag"]=2

                    if session["language"]==0:

                        session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

                    else:
                        session["flagText"]="Lütfen bağlantılarınızda http:// veya https:// protokollerinden birini belirtin."

                    return redirect(url_for("myApps.myApps"))

                linkCount+=1

            except:

                pass

            if linkCount==0:

                session["flag"]=2

                if session["language"]==0:

                    session["flagText"]="Please add at least one link to the application."

                else:
                    session["flagText"]="Lütfen uygulamaya en az bir bağlantı ekleyin."

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

            if (appNameInput!=appName) and (createQR==True):

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
            
            session["flag"]=0

            if session["language"]==0:

                session["flagText"]="Application update process successful."

            else:
                session["flagText"]="Uygulama güncelleme işlemi başarılı."

            return redirect(url_for("myApps.myApps"))


        else:

            session["flag"]=2

            if session["language"]==0:

                session["flagText"]="The application name must be between 3 and 30 characters."

            else:
                session["flagText"]="Uygulama adı 3 ile 30 karakter arasında olmalıdır."

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

            return render_template("/myApps.html", flag=flag, flagText=flagText, apps=apps, myUrl=myUrl, language=session["language"])

        else:

            return render_template("/myApps.html", apps=apps, myUrl=myUrl, language=session["language"])


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

            if session["language"]==0:

                session["flagText"]="Your app has been successfully deleted... ({})".format(appName)

            else:
                session["flagText"]="Uygulamanız başarıyla silindi... ({})".format(appName)

            return redirect(url_for("myApps.myApps"))

        except:

            session["flag"] = 2
            
            if session["language"]==0:

                session["flagText"]="Application deletion failed, unexpected error occurred."

            else:
                session["flagText"]="Uygulama silinemedi, beklenmeyen bir hata oluştu."

            return redirect(url_for("myApps.myApps"))

    else:

        return redirect(url_for("myApps.myApps"))
