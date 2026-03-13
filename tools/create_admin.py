import os
import sys
import sqlite3
from werkzeug.security import generate_password_hash

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.schema import DB_PATH, init_db

def create_admin_user(username, password):
    """
    指定されたユーザー名とパスワードで管理者アカウントを作成する。
    既に存在する場合はパスワードを更新する。
    """
    # データベース初期化（存在しない場合）
    init_db()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # パスワードをハッシュ化
    password_hash = generate_password_hash(password)
    
    try:
        # ユーザーが存在するか確認
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user:
            # 既存ユーザーのパスワードを更新
            cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (password_hash, username))
            print(f"User '{username}' already exists. Password updated.")
        else:
            # 新規ユーザーを作成
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            print(f"User '{username}' created successfully.")
            
        conn.commit()
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # 初期管理者アカウントの設定
    admin_username = "mat2002"
    admin_password = "math2026"  # 初期パスワード
    
    create_admin_user(admin_username, admin_password)
