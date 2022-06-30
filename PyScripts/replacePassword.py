from PyScripts.database import *
from flask import Blueprint
import socket
from flask import render_template, Flask, flash, request, logging, session, redirect, url_for
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyScripts.database import *
from datetime import datetime, timedelta
from PyScripts.token import generate_confirmation_token, confirm_token
import string
import random
from passlib.hash import sha256_crypt

replacePassBluePrint = Blueprint('replacePass', __name__,
                        template_folder='templates')

resetPassBluePrint = Blueprint('resetPass', __name__,
                        template_folder='templates')

@replacePassBluePrint.route("/replacePass",methods = ['GET', 'POST'])
def replacePass():

    if request.method == "POST":

        try:

            email = request.form['email']

            cursor.execute(
            'SELECT user_email, user_countattack FROM TBL_Users WHERE user_email=%s and user_isdeleted=%s and user_confirmed!=%s', (email, 0,0,))
            user = cursor.fetchall()
            email = user[0][0]
            user_countattack = user[0][1]

            if int(user_countattack)>10:

                cursor.execute('UPDATE TBL_Users SET user_isdeleted=1 WHERE user_email=%s',
				(email,))
                conn.commit()

                session["flag"] = 2
                session["flagText"] = "Mail sunucumuzda çok fazla işlem yaptığınız için saldırı olarak algıladık. Hesabınız devre dışı bırakılmıştır."
                return redirect(url_for("main"))


            else:

                cursor.execute('UPDATE TBL_Users SET user_countattack=%s WHERE user_email=%s',
				(int(user_countattack)+1, email,))
                conn.commit()

            try:

                token = generate_confirmation_token(email)

                token = myUrl+"resetPass/"+token

                strHtml = """
                
<p>Şifre Sıfırlama Bağlantısı:</p>
<p><a href="{}">{}</a></p>
<br>
<p>Cheers!</p>
        
    """.format(token, token)

                konu = "Password Reset Link"
                ileti = strHtml
                gonderenMail = 'softforrange@yandex.com'
                gonderilenMail = email
                sifre = sender_pass = 'sfr06580658'
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

                session["flag"] = 1
                session["flagText"] = "Şifre yenileme bağlantısı gönderildi, lütfen mail kutunuzu kontrol ediniz (bağlantı 10 dk geçerlilik süresine sahip)"
                return redirect(url_for("main"))

            except:

                return render_template("/PasswordSendMail.html", flag=2, flagText="Bir hata oluştu, lütfen tekrar deneyiniz.")


        except:

            return render_template("/PasswordSendMail.html", flag=2, flagText="Bu email adresine sahip kayıt bulunamadı.")


    else:

        return render_template("/PasswordSendMail.html")


@resetPassBluePrint.route("/resetPass/<token>",methods = ['GET', 'POST'])
def resetPass(token):

    flag = None

    try:

        print(session["user_id"])

    except:

        flag=True

    if flag==None:

        return redirect(url_for("myApps.myApps"))

    try:

        emailTemp = confirm_token(token)

        if emailTemp==False:

            session["flag"] = 2
            session["flagText"] = "Şifre yenilemede bir hata oluştu, lütfen tekrar deneyiniz."
		
            return redirect(url_for("main"))

        email = emailTemp.split("-")[0]
        email = str(email)

        dataTime = emailTemp.split("-")[1] 
        datetime_object = datetime.strptime(dataTime ,'%d/%m/%Y %H:%M:%S')

        now = datetime.now()

        new_final_time = datetime_object + timedelta(minutes=10)

        if now>=new_final_time:

            session["flag"] = 2
            session["flagText"] = "Bağlantının süresi doldu..."
		
            return redirect(url_for("main"))

		
        cursor.execute('SELECT user_id, user_countattack FROM TBL_Users WHERE user_email=%s',(email,))
        user = cursor.fetchall()
        user_id = user[0][0]
        user_countattack = user[0][1]

        if int(user_countattack)>10:

            cursor.execute('UPDATE TBL_Users SET user_isdeleted=1 WHERE user_email=%s',
			(email,))
            conn.commit()

            session["flag"] = 2
            session["flagText"] = "Mail sunucumuzda çok fazla işlem yaptığınız için saldırı olarak algıladık. Hesabınız devre dışı bırakılmıştır."
            
            return redirect(url_for("main"))


        else:

            cursor.execute('UPDATE TBL_Users SET user_countattack=%s WHERE user_email=%s',
			(int(user_countattack)+1, email,))
            conn.commit()

        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
        length = 20

        random.shuffle(characters)
	
        password = []
        for i in range(length):
            password.append(random.choice(characters))


        random.shuffle(password)

        listToStr = ''.join([str(elem) for elem in password])
        password = listToStr


        strHtml = """
                
<p>Yeni Şifre:</p>
<p>{}</p>
<br>
<p>Cheers!</p>
        
    """.format(password)

        konu = "New Password"
        ileti = strHtml
        gonderenMail = 'softforrange@yandex.com'
        gonderilenMail = email
        sifre = sender_pass = 'sfr06580658'
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

        password_hash = sha256_crypt.encrypt(password)

        cursor.execute('UPDATE TBL_Users SET user_password=%s WHERE user_id=%s',
        (password_hash,user_id,))
        conn.commit()

        session["flag"] = 0
        session["flagText"] = "Mail doğrulama başarılı, yeni şifreniz mail adresinize gönderilmiştir, bu şifre ile giriş yapıp profilinizden mevcut şifreyi değiştirebilirsiniz."
        return redirect(url_for("main"))

    except:

        session["flag"] = 2
        session["flagText"] = "Şifre yenilemede bir hata oluştu, lütfen tekrar deneyiniz."
		
        return redirect(url_for("main"))