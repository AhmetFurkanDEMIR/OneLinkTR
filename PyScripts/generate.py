import qrcode
from PyScripts.database import *
from flask import Blueprint
import socket
from flask import render_template, Flask, flash, request, logging, session, redirect, url_for


generateBluePrint = Blueprint('generate', __name__,
                        template_folder='templates')

@generateBluePrint.route('/generate', methods = ['GET', 'POST'])
@login_required
def generate():

	if request.method == "POST":

		cursor.execute(
            'SELECT user_appcount FROM TBL_Users WHERE user_id=%s', (session["user_id"],))
		user_appcount = cursor.fetchall()[0][0]

		if int(user_appcount)==2:

			session["flag"] = 2
			session["flagText"] = "Your right to create an application has expired."

			return redirect(url_for("create"))


		appName = str(request.form['appName'])

		notSTR="\"!'^+%&/()=?_-*\\,><;: "

		for i in notSTR:

			if str(i) in str(appName):

				session["flag"] = 2
				session["flagText"] = "Your application name must not contain \"{}\" character.".format(i)

				return redirect(url_for("create"))

				
		if len(str(appName)) > 3 and len(str(appName)) < 30:

			try:

				cursor.execute('SELECT app_id FROM TBL_Apps WHERE lower(app_name)=%s',(appName.lower(),))
				App_id = cursor.fetchall()
				App_id = App_id[0][0]

				if App_id!=None or len(App_id)!=0:

					session["flag"] = 2
					session["flagText"] = "This app name has been taken by someone else."

					return redirect(url_for("create"))

			except:

				pass

			linkCount = 0

			try:	

				apple = request.form['iosText']

				if len(apple) < 3 or len(apple) >130 :

					session["flag"] = 2
					session["flagText"] = "link size boyutu 3 ile 130 karakter arasında olmalıdır."

					return redirect(url_for("create"))
					
				flaga = "http://" in apple
				flagb = "https://" in apple

				if flaga!=True and flagb!=True:

					session["flag"] = 2
					session["flagText"] = "lütfen linklerinizde http:// veya https:// protokollerini belirtiniz"

					return redirect(url_for("create"))
				
				linkCount+=1

			except:
				pass


			try:

				android = request.form['androidText']

				if len(android) < 3 or len(android) >130 :
					
					session["flag"] = 2
					session["flagText"] = "link size boyutu 3 ile 130 karakter arasında olmalıdır."

					return redirect(url_for("create"))


				flaga = "http://" in android
				flagb = "https://" in android

				if flaga!=True and flagb!=True:

					session["flag"] = 2
					session["flagText"] = "lütfen linklerinizde http:// veya https:// protokollerini belirtiniz"

					return redirect(url_for("create"))

				linkCount+=1

			except:

				pass

			try:

				huawei = request.form['huaweiText']

				if len(huawei) < 3 or len(huawei) >130 :
					
					session["flag"] = 2
					session["flagText"] = "link size boyutu 3 ile 130 karakter arasında olmalıdır."

					return redirect(url_for("create"))


				flaga = "http://" in huawei
				flagb = "https://" in huawei

				if flaga!=True and flagb!=True:

					session["flag"] = 2
					session["flagText"] = "lütfen linklerinizde http:// veya https:// protokollerini belirtiniz"

					return redirect(url_for("create"))

				linkCount+=1

			except:

				pass

			try:

				windows = request.form['windowsText']

				if len(windows) < 3 or len(windows) >130 :
					
					session["flag"] = 2
					session["flagText"] = "link size boyutu 3 ile 130 karakter arasında olmalıdır."

					return redirect(url_for("create"))


				flaga = "http://" in windows
				flagb = "https://" in windows

				if flaga!=True and flagb!=True:

					session["flag"] = 2
					session["flagText"] = "lütfen linklerinizde http:// veya https:// protokollerini belirtiniz"

					return redirect(url_for("create"))

				linkCount+=1

			except:

				pass


			try:

				ubuntu = request.form['ubuntuText']

				if len(ubuntu) < 3 or len(ubuntu) >130 :
					
					session["flag"] = 2
					session["flagText"] = "link size boyutu 3 ile 130 karakter arasında olmalıdır."

					return redirect(url_for("create"))

				flaga = "http://" in ubuntu
				flagb = "https://" in ubuntu

				if flaga!=True and flagb!=True:

					session["flag"] = 2
					session["flagText"] = "lütfen linklerinizde http:// veya https:// protokollerini belirtiniz"

					return redirect(url_for("create"))

				linkCount+=1

			except:

				pass

			if linkCount==0:

				session["flag"] = 2
				session["flagText"] = "Please add at least one link to the application."

				return redirect(url_for("create"))

			cursor.execute('INSERT INTO TBL_Apps(user_id, app_name) VALUES(%s, %s)',(int(session["user_id"]),appName,))
			conn.commit()

			cursor.execute('SELECT app_id FROM TBL_Apps WHERE app_name=%s',(appName,))
			App_id = cursor.fetchall()
			App_id = App_id[0][0]

			try:
				
				try:
					apple=str(apple)
				except:

					apple = "-"

				cursor.execute('INSERT INTO TBL_Links(app_id, link_name, link_url) VALUES(%s, %s, %s)',(App_id,"Apple",apple,))
				conn.commit()

			except:

				pass

			try:

				try:
					android=str(android)
				except:

					android = "-"

				cursor.execute('INSERT INTO TBL_Links(app_id, link_name, link_url) VALUES(%s, %s, %s)',(App_id,"Android",android,))
				conn.commit()

			except:

				pass

			try:

				try:
					huawei=str(huawei)
				except:

					huawei = "-"

				cursor.execute('INSERT INTO TBL_Links(app_id, link_name, link_url) VALUES(%s, %s, %s)',(App_id,"Huawei",huawei,))
				conn.commit()

			except:

				pass

			try:

				try:
					windows=str(windows)
				except:

					windows = "-"

				cursor.execute('INSERT INTO TBL_Links(app_id, link_name, link_url) VALUES(%s, %s, %s)',(App_id,"Windows",windows,))
				conn.commit()

			except:

				pass

			try:

				try:
					ubuntu=str(ubuntu)
				except:

					ubuntu = "-"

				cursor.execute('INSERT INTO TBL_Links(app_id, link_name, link_url) VALUES(%s, %s, %s)',(App_id,"Ubuntu",ubuntu,))
				conn.commit()

			except:
				pass


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

			cursor.execute('UPDATE TBL_Users SET user_appcount=user_appcount+1 WHERE user_id=%s',
			(session["user_id"],))
			conn.commit()

			flagText = "You can access your application via a single link, regardless of device, from the link below."
			return render_template("/generate.html", flag=0, flagText=flagText, appName=appName, myUrl=myUrl)

		else:

			session["flag"] = 2
			session["flagText"] = "App title > 3 and App title <30"

			return redirect(url_for("create"))

	else:

		return redirect(url_for("create"))
