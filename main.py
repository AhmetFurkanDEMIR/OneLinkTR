from flask import render_template, Flask, flash, request, logging, session, redirect, url_for
from matplotlib.pyplot import flag
from PyScripts.database import *
from PyScripts.generate import generateBluePrint
from PyScripts.register import registerBluePrint, confirm_emailBluePrint
from PyScripts.myApps import myAppsBluePrint
from PyScripts.myApps import deleteAppBluePrint
from passlib.hash import sha256_crypt
from PyScripts.replacePassword import replacePassBluePrint, resetPassBluePrint

# Flask app
app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'static/uploads'
app.secret_key = b'_softforrange***d*'

app.register_blueprint(generateBluePrint)
app.register_blueprint(registerBluePrint)
app.register_blueprint(confirm_emailBluePrint)
app.register_blueprint(myAppsBluePrint)
app.register_blueprint(replacePassBluePrint)
app.register_blueprint(resetPassBluePrint)
app.register_blueprint(deleteAppBluePrint)

@app.route("/")
def main():

    try:

        session["flag"]

    except:

        session["flag"]=99

    flag = None

    try:

        print(session["user_id"])

    except:

        flag = True

    if flag == None:

        return redirect(url_for("myApps.myApps"))


    if session["flag"] != 99:

        flag = session["flag"]
        flagText = session["flagText"]

        session["flag"] = 99

        return render_template("/index.html", flag=flag, flagText=flagText)

    else:

        return render_template("/index.html")



@app.route("/login", methods=['GET', 'POST'])
def login():

    flag = None

    try:

        print(session["user_id"])

    except:

        flag = True

    if flag == None:

        return redirect(url_for("myApps.myApps"))

    if request.method == "POST":

        try:

            email = request.form['email']

            cursor.execute(
                'SELECT user_id, user_password, user_confirmed FROM TBL_Users WHERE user_email=%s and user_isdeleted=%s', (email, 0,))
            user = cursor.fetchall()
            user_id = user[0][0]
            user_password = user[0][1]
            user_confirmed = user[0][2]

            if int(user_confirmed) == 0:

                session["flag"]=2
                session["flagText"]="Maalesef hesabınız doğrulanmış durumda değil, lütfen mail adresinizdeki linke tıklayarak hesabınızı doğrulayınız."

                return redirect(url_for("login"))

        except:

            session["flag"]=2
            session["flagText"]="Kullanıcı Bulunamadı"

            return redirect(url_for("login"))

        password = request.form['pass']

        if sha256_crypt.verify(password, user_password) != True:

            session["flag"]=2
            session["flagText"]="Şifre hatalı"

            return redirect(url_for("login"))

        session["logged_in"] = True
        session["user_id"] = user_id

        session["flag"] = 0
        session["flagText"] = "Giriş Başarılı"

        return redirect(url_for("myApps.myApps"))

    else:

        if session["flag"] != 99:

            flag = session["flag"]
            flagText = session["flagText"]

            session["flag"] = 99

            return render_template("/login.html", flag=flag, flagText=flagText)

        else:

            return render_template("/login.html")



@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():

	session.clear()

	session["flag"] = 0
	session["flagText"] = "Çıkış Başarılı"

	return redirect(url_for("main"))


@app.route("/me", methods=['GET', 'POST'])
@login_required
def me():

	if request.method == "POST":

		try:

			deleteAccont = request.form['deleteAccont']

			if str(deleteAccont)=="1":

				cursor.execute(
				'SELECT user_password FROM TBL_Users WHERE user_id=%s and user_isdeleted=%s', (session["user_id"], 0,))
				user_password = cursor.fetchall()[0][0]

				passwordDelete = request.form['passwordDelete']

				if sha256_crypt.verify(passwordDelete, user_password) != True:

					session.clear()

					session["flag"] = 2
					session["flagText"] = "Şifre doğrulama başarısız, hesabınız silinemedi"

					return redirect(url_for("main"))
					

				else:

					cursor.execute('UPDATE TBL_Users SET user_isdeleted=%s WHERE user_id=%s',
					(1, session["user_id"],))
					conn.commit()

					session.clear()

					session["flag"] = 1
					session["flagText"] = "Hesabınız Başarıyla Silinmiştir...."

					return redirect(url_for("main"))
		except:

			pass

		ad = request.form['name']
		soyad = request.form['surname']
		password = request.form['password']
		newPassword = request.form['newPassword']

		cursor.execute(
		'SELECT user_password FROM TBL_Users WHERE user_id=%s and user_isdeleted=%s', (session["user_id"], 0,))
		user_password = cursor.fetchall()[0][0]

		if sha256_crypt.verify(password, user_password) != True:

			session.clear()

			session["flag"]=2
			session["flagText"]="Şifre doğrulama başarısız."

			return redirect(url_for("main"))


		if (len(str(ad))<3 or len(str(ad)) > 30) or (len(str(soyad))<3 or len(str(soyad)) > 30):

			session["flag"]=2
			session["flagText"]="Ad ve Soyad 3 karakterden küçük ve 30 karakterden büyük olamaz."

			return redirect(url_for("me"))

		if (len(str(newPassword)) < 8 or len(str(newPassword)) > 30) and (len(str(newPassword))!=0):

			session["flag"]=2
			session["flagText"]="Yeni şifreniz 8 ila 30 karakter arasında olmalıdır, lütfen tekrar deneyiniz."

			return redirect(url_for("me"))

		if len(str(newPassword))!=0:

			newPassword = sha256_crypt.encrypt(newPassword)

			cursor.execute('UPDATE TBL_Users SET user_name=%s, user_surname=%s, user_password=%s WHERE user_id=%s',
			(ad, soyad, newPassword, session["user_id"],))
			conn.commit()

		else:
			cursor.execute('UPDATE TBL_Users SET user_name=%s, user_surname=%s WHERE user_id=%s',
			(ad, soyad, session["user_id"],))
			conn.commit()

		session["flag"]=0
		session["flagText"]="Profil güncelleme başarılı."

		return redirect(url_for("me"))

	else:

		cursor.execute(
        'SELECT * FROM TBL_Users WHERE user_id=%s and user_isdeleted=%s', (session["user_id"], 0,))
		user = cursor.fetchall()

		user_final = []

		for i in user[0]:

			user_final.append(i)

		user_final[3] = int(user_final[3])
		del user_final[0]
		del user_final[4]
		del user_final[4]
		del user_final[4]

		if session["flag"] != 99:

			flag = session["flag"]
			flagText = session["flagText"]

			session["flag"] = 99

			return render_template("/me.html", user_final=user_final, flag=flag, flagText=flagText)

		return render_template("/me.html", user_final=user_final)


@app.route("/create")
@login_required
def create():

	cursor.execute('SELECT user_appcount FROM TBL_Users WHERE user_id=%s',(session["user_id"],))
	count = cursor.fetchall()
	count = count[0][0]

	count = 2 - int(count)

	if session["flag"] != 99:

		flag = session["flag"]
		flagText = session["flagText"]

		session["flag"] = 99

		return render_template("/create.html", count=count,flag=flag, flagText=flagText,)
	
	else:
		return render_template("/create.html", count=count)


@app.route("/<string:name>")
def runLink(name):

    try:

        cursor.execute(
            'SELECT app_id FROM TBL_Apps WHERE app_name=%s', (name,))
        App_id = cursor.fetchall()
        App_id = App_id[0][0]

    except:

        # error hazirla
        return render_template("/index.html", flag=77)

    ios = myUrl
    android = myUrl
    windows = myUrl
    ubuntu = myUrl
    huawei = myUrl

    cursor.execute(
        'SELECT link_name, link_url FROM TBL_Links WHERE app_id=%s', (App_id,))
    Links = cursor.fetchall()

    for i in Links:

        if (i[0] == "Apple") and (i[1]!="-"):

            ios = i[1]

        elif (i[0] == "Huawei") and (i[1]!="-"):

            huawei = i[1]

        elif (i[0] == "Windows") and (i[1]!="-"):

            windows = i[1]

        elif (i[0] == "Ubuntu") and (i[1]!="-"):

            ubuntu = i[1]

        elif (i[0] == "Android") and (i[1]!="-"):

            android = i[1]

    html = """

		<!DOCTYPE html>
		<html>
		<head>
		    <meta name="viewport" content="width=device-width, initial-scale=1">
		    <meta charset="utf-8" />
		    <title></title>
		</head>

			<script>

				function getOS() {
				  var userAgent = window.navigator.userAgent,
				      platform = window.navigator?.userAgentData?.platform ?? window.navigator.platform,
				      macosPlatforms = ['Macintosh', 'MacIntel', 'MacPPC', 'Mac68K'],
				      windowsPlatforms = ['Win32', 'Win64', 'Windows', 'WinCE'],
				      huaweiPlatforms = ['HUAWEI'],
				      iosPlatforms = ['iPhone', 'iPad', 'iPod'],
				      os = null;

				  if (macosPlatforms.indexOf(platform) !== -1) {
				    window.location.replace(\""""+ios+"""\");
				  } else if (iosPlatforms.indexOf(platform) !== -1) {
				    window.location.replace(\""""+ios+"""\");
				  } else if (windowsPlatforms.indexOf(platform) !== -1) {
				    window.location.replace(\""""+windows+"""\");
				  } else if (/Android/.test(userAgent)) {
				    window.location.replace(\""""+android+"""\");
				  } else if (!os && /Linux/.test(platform)) {
				    window.location.replace(\""""+ubuntu+"""\");
				  } else if (!os && /Huawei/.test(platform)) {
				    window.location.replace(\""""+huawei+"""\");
				  }


				}

				getOS();

			</script> 

		</html>


		"""

    return html


if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port=5600)
