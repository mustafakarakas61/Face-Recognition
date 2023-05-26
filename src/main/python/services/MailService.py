import base64
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.main.python.services.DatabaseService import findUser
from utils.Utils import randomInt, randomString


def newUser(username, user_mail, user_name, user_surname):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()

        server.login(os.getenv('SENDER_MAIL'), base64.b64decode(os.getenv('SENDER_MAIL_PASS')).decode('utf-8'))

        securityCode: int = randomInt(6)

        email = MIMEMultipart()
        email['From'] = os.getenv('SENDER_MAIL')
        email['To'] = user_mail
        email['Subject'] = "Yeni Kayıt"

        message = f"""
        Merhaba {user_name} {user_surname},<br>
        <br>
        Kullanıcı Adınız: <strong>{username}</strong><br>
        <br>
        Kaydınızı onaylamak için aşağıdaki kodu sisteme giriniz.<br>
        <br>
        Güvenlik Kodu: <strong>{securityCode}</strong><br>
        <br>
        Daha fazla yardıma ihtiyacınız varsa, lütfen bize ulaşın.<br>
        <br>
        Saygılarımızla,<br>
        Mustafa Karakaş
        """

        email.attach(MIMEText(message, 'html'))

        server.sendmail(os.getenv('SENDER_MAIL'), user_mail, email.as_string())

        return securityCode
    except Exception as e:
        return None
    finally:
        server.quit()


def renewPassword(username):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    try:
        user_id, user_mail, user_name, user_surname, user_role = findUser(username)
        if user_id is None or user_mail is None or user_name is None or user_surname is None or user_role is None:
            return None
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.ehlo()
            server.starttls()

            server.login(os.getenv('SENDER_MAIL'), base64.b64decode(os.getenv('SENDER_MAIL_PASS')).decode('utf-8'))

            securityCode: int = randomInt(6)

            email = MIMEMultipart()
            email['From'] = os.getenv('SENDER_MAIL')
            email['To'] = user_mail
            email['Subject'] = "Şifre Yenileme Talebi"

            message = f"""
            Merhaba {user_name} {user_surname},<br>
            <br>
            Kullanıcı Adınız: <strong>{username}</strong><br>
            <br>
            Şifrenizi onaylamak için aşağıdaki kodu sisteme giriniz.<br>
            <br>
            Güvenlik Kodu: <strong>{securityCode}</strong><br>
            <br>
            Daha fazla yardıma ihtiyacınız varsa, lütfen bize ulaşın.<br>
            <br>
            Saygılarımızla,<br>
            Mustafa Karakaş
            """

            email.attach(MIMEText(message, 'html'))

            server.sendmail(os.getenv('SENDER_MAIL'), user_mail, email.as_string())

            return securityCode
    except Exception as e:
        return None
    finally:
        server.quit()


def forgetPassword(username):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    try:
        user_id, user_mail, user_name, user_surname, user_role = findUser(username)
        if user_id is None or user_mail is None or user_name is None or user_surname is None or user_role is None:
            return None
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.ehlo()
            server.starttls()

            server.login(os.getenv('SENDER_MAIL'), base64.b64decode(os.getenv('SENDER_MAIL_PASS')).decode('utf-8'))

            securityCode = ""
            securityCode += str(randomString(2))
            securityCode += str(randomInt(2))
            securityCode += str(randomString(2))
            securityCode += str(randomInt(2))
            securityCode += str(randomString(2))
            securityCode += str(randomInt(2))
            securityCode += str(randomString(2))
            securityCode += str(randomInt(2))

            email = MIMEMultipart()
            email['From'] = os.getenv('SENDER_MAIL')
            email['To'] = user_mail
            email['Subject'] = "Şifre Sıfırlama Talebi"

            message = f"""
            Merhabalar {user_name} {user_surname},<br>
            <br>
            Şifrenizi sıfırlamak için bu e-postayı gönderiyoruz.<br>
            <br>
            Kullanıcı Adınız: <strong>{username}</strong><br>
            <br>
            Güvenlik Kodu: <strong>{securityCode}</strong><br>
            <br>
            Daha fazla yardıma ihtiyacınız varsa, lütfen bize ulaşın.<br>
            <br>
            Saygılarımızla,<br>
            Mustafa Karakaş
            """

            email.attach(MIMEText(message, 'html'))

            server.sendmail(os.getenv('SENDER_MAIL'), user_mail, email.as_string())

            return securityCode
    except Exception as e:
        return None
    finally:
        server.quit()
