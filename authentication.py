import hashlib
import database as database
import smtplib, ssl
from tkinter import Entry
import string
import random
from tkinter import messagebox
from email.message import EmailMessage

sender = 'mydiarygcmanager@gmail.com'
password = 'mydiary123$'
port = 465

user_access = dict()


def encrypt_password(password):
    encoded = password.encode()
    return str(hashlib.sha256(encoded).hexdigest())


def login(username, password):
    encrypted_password = encrypt_password(password)
    args = database.get_user_info(username)
    if args is None:
        return

    retrieved_password = args[1]
    return encrypted_password == retrieved_password


def send_recover_email(username):
    email = database.get_email(username)

    if email is None or email == '':
        messagebox.showerror('Error', 'Account doesnt exist')
        return False

    digits = string.digits
    code = ''.join(random.choice(digits) for i in range(5))
    user_access[username] = code
    context = ssl.create_default_context()
    msg = EmailMessage()
    msg.set_content("Your MyDiary account recovery code: "+str(code))
    msg["Subject"] = "Account recovery"
    msg["From"] = sender
    msg["To"] = email
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
            smtp.starttls(context=context)
            smtp.login(msg["From"], password)
            smtp.send_message(msg)
            return True
    except:
        messagebox.showerror('Error', 'The email provided is not valid')
        return False


def verify_access_code(username, entry):
    code = user_access.get(username)
    print(code)
    submitted = entry.get()
    print(submitted)
    return submitted == code


def update_password(username, entry):
    password = entry.get()
    if password is None or password == '':
        return False

    password = encrypt_password(password)
    database.set_password(username, password)
    return True



