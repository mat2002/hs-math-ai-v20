import sqlite3
import os
from flask_login import UserMixin
from database.schema import DB_PATH

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

def get_user_by_id(user_id):
    """
    IDからユーザー情報を取得する。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return User(id=row[0], username=row[1], email=row[2])
    return None

def get_user_by_username(username):
    """
    ユーザー名からユーザー情報を取得する。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return User(id=row[0], username=row[1], email=row[2])
    return None
