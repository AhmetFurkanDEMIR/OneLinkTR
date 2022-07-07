from flask import Blueprint
from passlib.hash import sha256_crypt
from PyScripts.token import generate_confirmation_token, confirm_token
from flask import render_template, request, redirect, url_for
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyScripts.tools import *
from datetime import datetime, timedelta

registerBluePrint = Blueprint('register', __name__,
                        template_folder='templates')

@registerBluePrint.route("/register",methods = ['GET', 'POST'])
def register():

	flag = None

	try:

		print(session["user_id"])

	except:

		flag=True

	if flag==None:

		return redirect(url_for("myApps.myApps"))

	if request.method == "POST":

		if recaptcha.verify()==False:

			session["flag"]=2

			if session["language"]==0:

				session["flagText"]="We were unable to confirm that you are human."

			else:
				session["flagText"]="İnsan olduğunuzu doğrulayamadık."

			return redirect(url_for("main"))

		try:

			ad = request.form['adi']
			soyad = request.form['soyadi']
			email = request.form['email']
			tel = request.form['tel']
			password = request.form['password']
			passworda = request.form['passworda']

			if (len(str(ad))<3 or len(str(ad)) > 30) or (len(str(soyad))<3 or len(str(soyad)) > 30):

				session["flag"] = 2
				
				if session["language"]==0:

					session["flagText"] = "Name and Surname cannot be less than 3 characters and larger than 30 characters."

				else:
					
					session["flagText"] = "Ad ve Soyad 3 karakterden az 30 karakterden büyük olamaz."

				return redirect(url_for("register.register"))

			if len(str(tel)) != 10:

				session["flag"] = 2

				if session["language"]==0:

					session["flagText"] = "phone number must be ten digits without leading \"0\" and no spaces"

				else:
					
					session["flagText"] = "telefon numarası, başında \"0\" olmadan ve boşluk olmadan on haneden oluşmalıdır"

				return redirect(url_for("register.register"))

			if (len(str(password)) < 8 or len(str(password)) > 30) or (len(str(passworda)) < 8 or len(str(passworda)) > 30):

				session["flag"] = 2

				if session["language"]==0:

					session["flagText"] = "Your password must be between 8 and 30 characters, please try again."

				else:
					
					session["flagText"] = "Şifreniz 8 ile 30 karakter arasında olmalıdır, lütfen tekrar deneyiniz."

				return redirect(url_for("register.register"))


			if ("@gmail.com" in email) == False:

				session["flag"] = 2

				if session["language"]==0:

					session["flagText"] = "Since our project is still in beta, we only allow google mails with gmail extensions."

				else:
					
					session["flagText"] = "Projemiz henüz beta sürümünde olduğu için yalnızca gmail uzantılı google maillerine izin veriyoruz."

				return redirect(url_for("register.register"))

			if len(str(email)) < 5 or len(str(email))>50:

				session["flag"] = 2

				if session["language"]==0:

					session["flagText"] = "Incorrect email"

				else:
					
					session["flagText"] = "Hatalı mail"

				return redirect(url_for("register.register"))

		except:

			session["flag"] = 2

			if session["language"]==0:

				session["flagText"] = "Missing data has been entered, please fill in all the boxes."

			else:
					
				session["flagText"] = "Eksik veriler girildi, lütfen tüm kutuları doldurun."

			return redirect(url_for("register.register"))


		if password!=passworda:

			session["flag"] = 2

			if session["language"]==0:

				session["flagText"] = "The two passwords you entered are not the same, please try again."

			else:
					
				session["flagText"] = "Girdiğiniz iki şifre aynı değil, lütfen tekrar deneyin."

			return redirect(url_for("register.register"))

		try:

			password=sha256_crypt.encrypt(password)
            
			try:

				cursor.execute(
				'SELECT * FROM TBL_Users WHERE user_email=%s or user_phone=%s', (email, tel,))
				user = cursor.fetchall()
				user_id = user[0][0]

				session["flag"] = 2

				if session["language"]==0:

					session["flagText"] = "This Email or Phone number has been used before, please try again."

				else:
						
					session["flagText"] = "Bu E-posta veya Telefon numarası daha önce kullanılmış, lütfen tekrar deneyin."

				return redirect(url_for("register.register"))

			except:

				cursor.execute(
					'INSERT INTO TBL_Users(user_name, user_surname, user_phone, user_email, user_password, user_isdeleted, user_confirmed, user_countattack, user_appcount) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
					(ad, soyad, tel, email, password, 0, 0, 0,0,))
				conn.commit()

			token = generate_confirmation_token(email)

			token = myUrl+"confirm/"+token

			strHtml = """
			
<p>Welcome! Thanks for signing up. Please follow this link to activate your account.</p>
<p>Verification link (The validity period of the link is 30 minutes): <a href="{}">{}</a></p>
<br>
<p><a href="https://onelinktr.com/">OneLinkTR</a> | <a href="https://softforrange.com/">SoftForRange</a></p>
<br>
""".format(token, token)

			konu = "Mail Verification"
			ileti = strHtml
			gonderenMail = MyEmail
			gonderilenMail = email
			sifre = MyEmailPass
			message = MIMEMultipart()
			message["From"] = gonderenMail
			message["To"] = gonderilenMail
			message["Subject"] = konu
			message["Bcc"] = gonderilenMail
			message.attach(MIMEText(ileti, "html"))
			yazi = message.as_string()
			context = ssl.create_default_context()

			with smtplib.SMTP_SSL("smtp.yandex.com", 465, context=context) as server:
				server.login(gonderenMail, sifre)
				server.sendmail(gonderenMail, gonderilenMail, yazi)

		except:

			session["flag"] = 2

			if session["language"]==0:

				session["flagText"] = "An error was encountered during registration, please try again."

			else:
					
				session["flagText"] = "Kayıt sırasında bir hatayla karşılaşıldı, lütfen tekrar deneyin."

			return redirect(url_for("register.register"))

		session["flag"] = 0
		
		if session["language"]==0:

			session["flagText"] = "Email verification step, please go to your \""+email+"\" email address and click on the verification link (connection validity 30 minutes). Then your account will be activated and you will be able to use TekLink application."

		else:
					
			session["flagText"] = "E-posta doğrulama adımı, lütfen \""+email+"\" e-posta adresinize gidin ve doğrulama bağlantısını tıklayın (bağlantı geçerliliği 30 dakika). Ardından hesabınız aktif hale gelecek ve TekLink uygulamasını kullanabileceksiniz."
		
		return redirect(url_for("main"))


	else:


		if session["flag"] != 99:

			flag = session["flag"]
			flagText = session["flagText"]

			session["flag"] = 99

			return render_template("/register.html", flag=flag, flagText=flagText, language=session["language"])

		else:

			return render_template("/register.html", language=session["language"])


confirm_emailBluePrint = Blueprint('confirm_email', __name__,
                        template_folder='templates')

@confirm_emailBluePrint.route("/confirm/<token>")
def confirm_email(token):

	try:

		session["language"]

	except:

		session["language"]=0

	flag = None

	try:

		session["user_id"]

	except:

		flag=True

	if flag==None:

		return redirect(url_for("myApps.myApps"))

	try:

		emailTemp = confirm_token(token)


		if emailTemp==False:

			session["flag"] = 2

			if session["language"]==0:

				session["flagText"] = "An error occurred during the validation phase, please try again."

			else:
				
				session["flagText"] = "Doğrulama aşamasında bir hata oluştu, lütfen tekrar deneyin."
		
			return redirect(url_for("main"))

		email = emailTemp.split("-")[0]
		email = str(email)

		dataTime = emailTemp.split("-")[1]
		datetime_object = datetime.strptime(dataTime ,'%d/%m/%Y %H:%M:%S')

		now = datetime.now()

		new_final_time = datetime_object + timedelta(minutes=30)

		if now>=new_final_time:

			session["flag"] = 2

			if session["language"]==0:

				session["flagText"] = "The link has expired..."

			else:
				
				session["flagText"] = "Bağlantının süresi doldu..."
		
			return redirect(url_for("main"))

		
		cursor.execute('SELECT user_id, user_confirmed FROM TBL_Users WHERE user_email=%s and user_isdeleted=0',(email,))
		user = cursor.fetchall()
		user_id = user[0][0]
		user_confirmed = user[0][1]

		if user_confirmed==1:

			session["flag"] = 1

			if session["language"]==0:

				session["flagText"] = "Your account is already verified."

			else:
				
				session["flagText"] = "Hesabınız zaten doğrulandı."
		
			return redirect(url_for("main"))

		cursor.execute('UPDATE TBL_Users SET user_confirmed=%s WHERE user_id=%s',
		(1,user_id,))
		conn.commit()


		session["flag"] = 0

		if session["language"]==0:

			session["flagText"] = "Email verification is successful, you can now log in to your account."

		else:
				
			session["flagText"] = "E-posta doğrulaması başarılı, şimdi hesabınıza giriş yapabilirsiniz."

		return redirect(url_for("main"))


	except:

		session["flag"] = 2

		if session["language"]==0:

			session["flagText"] = "An error occurred during the validation phase, please try again."

		else:
				
			session["flagText"] = "Doğrulama aşamasında bir hata oluştu, lütfen tekrar deneyin."
		
		return redirect(url_for("main"))
        

