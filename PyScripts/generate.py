import qrcode
from PyScripts.tools import *
from flask import Blueprint

from flask import render_template, request, session, redirect, url_for


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

			if session["language"]==0:

				session["flagText"]="Your right to create an application has expired."

			else:
				session["flagText"]="Uygulama oluşturma hakkınız sona erdi."

			return redirect(url_for("create"))


		appName = str(request.form['appName'])

		blackList = ["login", "register", "home", "replacePass", "myApps", "create", "generate", "me", "tr", "en", "confirm", "resetPass", "logout","demir", "demirai", "sfr", "softforrange"]

		for i in blackList:

			if appName.lower()==i.lower():

				session["flag"]=2

				if session["language"]==0:

					session["flagText"]="You can't get this app name."

				else:
					session["flagText"]="Bu uygulama adını alamazsınız."

				return redirect(url_for("create"))


		if appName.isalnum()==False:

			session["flag"]=2
			if session["language"]==0:

				session["flagText"]="Your application name must not contain non-alphanumeric characters."

			else:
				session["flagText"]="Uygulama adınız alfanumerik olmayan karakterler içermemelidir."

			return redirect(url_for("create"))

		notSTR="\"!'^+%&/()=?_-*\\,><;:.é£#$½¾\{\}[]çıüğöşİĞÜÖŞÇ "

		for i in notSTR:

			if str(i) in str(appName):

				session["flag"]=2
				if session["language"]==0:

					session["flagText"]="Your application name must not contain \"{}\" character.".format(i)

				else:
					session["flagText"]="Uygulama adınız \"{}\" karakterini içermemelidir.".format(i)

				return redirect(url_for("myApps.myApps"))

		if len(str(appName)) > 3 and len(str(appName)) < 30:

			try:

				cursor.execute('SELECT app_id FROM TBL_Apps WHERE lower(app_name)=%s',(appName.lower(),))
				App_id = cursor.fetchall()
				App_id = App_id[0][0]

				if App_id!=None or len(App_id)!=0:

					session["flag"] = 2

					if session["language"]==0:
    
						session["flagText"]="This app name is being used by someone else, please try another app name."

					else:
						session["flagText"]="Bu uygulama adı başka biri tarafından kullanılıyor, lütfen başka bir uygulama adı deneyin."

					return redirect(url_for("create"))

			except:

				pass

			linkCount = 0

			try:	

				apple = request.form['iosText']

				if len(apple) < 3 or len(apple) >130 :

					session["flag"] = 2
					if session["language"]==0:

						session["flagText"]="The link length must be between 3 and 130 characters."

					else:
						session["flagText"]="Bağlantı uzunluğu 3 ile 130 karakter arasında olmalıdır."

					return redirect(url_for("create"))
					
				flaga = "http://" in apple
				flagb = "https://" in apple

				if flaga!=True and flagb!=True:

					session["flag"] = 2
					if session["language"]==0:

						session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

					else:
						session["flagText"]="Lütfen bağlantılarınızda http:// veya https:// protokollerinden birini belirtin."

					return redirect(url_for("create"))
				
				linkCount+=1

			except:
				pass


			try:

				android = request.form['androidText']

				if len(android) < 3 or len(android) >130 :
					
					session["flag"] = 2
					if session["language"]==0:

						session["flagText"]="The link length must be between 3 and 130 characters."

					else:
						session["flagText"]="Bağlantı uzunluğu 3 ile 130 karakter arasında olmalıdır."

					return redirect(url_for("create"))


				flaga = "http://" in android
				flagb = "https://" in android

				if flaga!=True and flagb!=True:

					session["flag"] = 2
					if session["language"]==0:

						session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

					else:
						session["flagText"]="Lütfen bağlantılarınızda http:// veya https:// protokollerinden birini belirtin."

					return redirect(url_for("create"))

				linkCount+=1

			except:

				pass

			try:

				huawei = request.form['huaweiText']

				if len(huawei) < 3 or len(huawei) >130 :
					
					session["flag"] = 2
					if session["language"]==0:

						session["flagText"]="The link length must be between 3 and 130 characters."

					else:
						session["flagText"]="Bağlantı uzunluğu 3 ile 130 karakter arasında olmalıdır."

					return redirect(url_for("create"))


				flaga = "http://" in huawei
				flagb = "https://" in huawei

				if flaga!=True and flagb!=True:

					session["flag"] = 2
					if session["language"]==0:

						session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

					else:
						session["flagText"]="Lütfen bağlantılarınızda http:// veya https:// protokollerinden birini belirtin."

					return redirect(url_for("create"))

				linkCount+=1

			except:

				pass

			try:

				windows = request.form['windowsText']

				if len(windows) < 3 or len(windows) >130 :
					
					session["flag"] = 2
					if session["language"]==0:

						session["flagText"]="The link length must be between 3 and 130 characters."

					else:
						session["flagText"]="Bağlantı uzunluğu 3 ile 130 karakter arasında olmalıdır."

					return redirect(url_for("create"))


				flaga = "http://" in windows
				flagb = "https://" in windows

				if flaga!=True and flagb!=True:

					session["flag"] = 2
					if session["language"]==0:

						session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

					else:
						session["flagText"]="Lütfen bağlantılarınızda http:// veya https:// protokollerinden birini belirtin."

					return redirect(url_for("create"))

				linkCount+=1

			except:

				pass


			try:

				ubuntu = request.form['ubuntuText']

				if len(ubuntu) < 3 or len(ubuntu) >130 :
					
					session["flag"] = 2
					if session["language"]==0:

						session["flagText"]="The link length must be between 3 and 130 characters."

					else:
						session["flagText"]="Bağlantı uzunluğu 3 ile 130 karakter arasında olmalıdır."

					return redirect(url_for("create"))

				flaga = "http://" in ubuntu
				flagb = "https://" in ubuntu

				if flaga!=True and flagb!=True:

					session["flag"] = 2
					if session["language"]==0:

						session["flagText"]="Please specify one of the http:// or https:// protocols in your links."

					else:
						session["flagText"]="Lütfen bağlantılarınızda http:// veya https:// protokollerinden birini belirtin."

					return redirect(url_for("create"))

				linkCount+=1

			except:

				pass

			if linkCount==0:

				session["flag"] = 2
				if session["language"]==0:

					session["flagText"]="Please add at least one link to the application."

				else:
					session["flagText"]="Lütfen uygulamaya en az bir bağlantı ekleyin."

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

			if session["language"]==0:

				flagText = "You can access your application via a single link, regardless of device, from the link below."

			else:
				flagText = "Uygulamanıza aşağıdaki linkten cihaz fark etmeksizin tek bir link üzerinden ulaşabilirsiniz."

			return render_template("/generate.html", flag=0, flagText=flagText, appName=appName, myUrl=myUrl, language=session["language"])

		else:

			session["flag"]=2

			if session["language"]==0:

				session["flagText"]="The application name must be between 3 and 30 characters."

			else:
				session["flagText"]="Uygulama adı 3 ile 30 karakter arasında olmalıdır."


			return redirect(url_for("create"))

	else:

		return redirect(url_for("create"))
