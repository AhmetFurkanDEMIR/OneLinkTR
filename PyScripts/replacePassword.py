from PyScripts.tools import *
from flask import Blueprint
from flask import render_template, request, redirect, url_for
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyScripts.tools import *
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
            'SELECT user_email, user_countattack FROM TBL_Users WHERE user_email=%s and user_isdeleted=%s and user_confirmed!=%s', (email, 0,0,))
            user = cursor.fetchall()
            email = user[0][0]
            user_countattack = user[0][1]

            if int(user_countattack)>10:

                cursor.execute('UPDATE TBL_Users SET user_isdeleted=1 WHERE user_email=%s',
				(email,))
                conn.commit()

                session["flag"] = 2
                session["flagText"] = "We have detected it as an attack because you are doing too many operations on our mail server. Your account has been disabled."
                return redirect(url_for("main"))


            else:

                cursor.execute('UPDATE TBL_Users SET user_countattack=%s WHERE user_email=%s',
				(int(user_countattack)+1, email,))
                conn.commit()

            try:

                token = generate_confirmation_token(email)

                token = myUrl+"resetPass/"+token

                strHtml = """
                
<p>Password Reset Link.</p>
<p>Link (The validity period of the connection is 30 minutes) : <a href="{}">{}</a></p>
<br>
<p><a href="https://teklink.com/">TekLink</a> | <a href="https://softforrange.com/">SoftForRange</a></p>
        
    """.format(token, token)

                konu = "Password Reset Link"
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

                session["flag"] = 0
                session["flagText"] = "Password reset link has been sent, please check your mailbox. The link may be delayed, please wait. (link is valid for 30 minutes)"
                return redirect(url_for("main"))

            except:

                session["flag"] = 2
                session["flagText"] = "An error has occurred, please try again."
                return redirect(url_for("replacePass.replacePass"))


        except:

            session["flag"] = 2
            session["flagText"] = "No user found with this email address."
            return redirect(url_for("replacePass.replacePass"))


    else:

        if session["flag"] != 99:

            flag = session["flag"]
            flagText = session["flagText"]

            session["flag"] = 99

            return render_template("/PasswordSendMail.html", flag=flag, flagText=flagText, language=session["language"])

        else:

            return render_template("/PasswordSendMail.html", language=session["language"])


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
            session["flagText"] = "There was an error resetting the password, please try again."
		
            return redirect(url_for("main"))

        email = emailTemp.split("-")[0]
        email = str(email)

        dataTime = emailTemp.split("-")[1] 
        datetime_object = datetime.strptime(dataTime ,'%d/%m/%Y %H:%M:%S')

        now = datetime.now()

        new_final_time = datetime_object + timedelta(minutes=30)

        if now>=new_final_time:

            session["flag"] = 2
            session["flagText"] = "The link has expired..."
		
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
            session["flagText"] = "We have detected it as an attack because you are doing too many operations on our mail server. Your account has been disabled."
            
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
                
<p>New Password: {}</p>
<br>
<p><a href="https://teklink.com/">TekLink</a> | <a href="https://softforrange.com/">SoftForRange</a></p>
        
    """.format(password)

        konu = "New Password"
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

        password_hash = sha256_crypt.encrypt(password)

        cursor.execute('UPDATE TBL_Users SET user_password=%s WHERE user_id=%s',
        (password_hash,user_id,))
        conn.commit()

        session["flag"] = 0
        session["flagText"] = "Mail verification is successful, your new password has been sent to your e-mail address, you can log in with this password and change the current password from your profile."
        return redirect(url_for("main"))

    except:

        session["flag"] = 2
        session["flagText"] = "There was an error resetting the password, please try again."
		
        return redirect(url_for("main"))