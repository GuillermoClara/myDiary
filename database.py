import sqlite3
from tkinter import messagebox
import authentication
from datetime import date

database_file_name = 'database'
user_table = 'users'
diary_table = 'diaries'


connection = None


def init():
    open_database()
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS '+user_table+'(username TEXT, password TEXT, email TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS '+diary_table+"(name TEXT, author TEXT, contents TEXT, date TEXT)")
    connection.close()


def open_database():
    global connection
    connection = sqlite3.connect(database_file_name)


def register_user(username, password, email):
    open_database()

    if already_exists_user(username):
        messagebox.showerror('Error', 'The username is already in use!')
        return False

    if already_exists_email(email):
        messagebox.showerror('Error', 'The e-mail is already in use!')
        return False

    encrypted_password = authentication.encrypt_password(password)

    cursor = connection.cursor()
    cursor.execute('INSERT INTO '+user_table+' VALUES(?,?,?)', (username, encrypted_password, email))
    connection.commit()

    return True


def already_exists_user(username):
    cursor = connection.cursor()
    cursor.execute('SELECT count(*) from '+user_table+" where username=?", [username])
    amount = int(cursor.fetchone()[0])
    return amount > 0


def already_exists_email(email):
    cursor = connection.cursor()
    cursor.execute('SELECT count(*) from '+user_table+' where email=?',[email])
    amount = int(cursor.fetchone()[0])
    return amount > 0


def get_user_info(username):
    open_database()
    if not already_exists_user(username):
        messagebox.showerror('Error', 'The account with this name doesnt exist!')
        return None

    cursor = connection.cursor()
    cursor.execute('SELECT * from '+user_table+' where username=?', [username])
    args = cursor.fetchone()
    connection.close()
    return args


def get_user_diaries(username):
    open_database()
    cursor = connection.cursor()
    cursor.execute('SELECT * from '+diary_table+" where author=?", [username])
    return cursor.fetchall()


def create_diary(name,username):
    created_date = date.today()
    open_database()
    cursor = connection.cursor()
    values = (name, username, '', created_date)
    cursor.execute('INSERT INTO '+diary_table+' VALUES(?,?,?,?)', values)
    connection.commit()
    connection.close()


def save_diary(name, username, text):
    open_database()
    cursor = connection.cursor()
    text_parsed = text.replace('\n', '{end_line}')
    values = (text_parsed, name, username)
    cursor.execute('UPDATE '+diary_table+" set contents=? WHERE author=? AND name=?", values)
    connection.commit()
    connection.close()


def remove_diary(name,username):
    open_database()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM '+diary_table+' WHERE name=? AND author=?', (name, username))
    connection.commit()
    connection.close()


def get_email(username):
    open_database()
    cursor = connection.cursor()
    cursor.execute('SELECT email FROM '+user_table+' WHERE username=?', [username])
    result = cursor.fetchone()
    if result is not None:
        result = cursor.fetchone()[0]
    connection.close()

    return result


def set_password(username, password):
    open_database()
    cursor = connection.cursor()
    cursor.execute('UPDATE '+user_table+" SET password=? WHERE username=?", (password, username))
    connection.commit()
    connection.close()
