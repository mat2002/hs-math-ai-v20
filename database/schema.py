import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'problems.db')

def init_db():
    """
    データベースとテーブルを初期化する。
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 問題テーブル（既存）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit TEXT NOT NULL,
        topic TEXT NOT NULL,
        difficulty INTEGER NOT NULL,
        problem_text TEXT NOT NULL,
        solution_text TEXT NOT NULL,
        answer_key TEXT NOT NULL,
        figure_code TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # ユーザーテーブル（新規）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 生成履歴テーブル（新規）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS generation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        doc_type TEXT NOT NULL,
        unit TEXT NOT NULL,
        difficulty INTEGER NOT NULL,
        pdf_filename TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # インデックス
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_unit_topic ON problems(unit, topic)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_history ON generation_history(user_id)')
    
    conn.commit()
    conn.close()

def create_user(username, password, email=None):
    """
    新しいユーザーを作成する。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        cursor.execute('INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)', 
                       (username, password_hash, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    """
    ユーザーの認証を行う。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], password):
        return user[0]  # user_id を返す
    return None

def save_generation_history(user_id, doc_type, unit, difficulty, pdf_filename):
    """
    生成履歴を保存する。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO generation_history (user_id, doc_type, unit, difficulty, pdf_filename)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, doc_type, unit, difficulty, pdf_filename))
    conn.commit()
    conn.close()

def get_user_history(user_id):
    """
    ユーザーの生成履歴を取得する。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, doc_type, unit, difficulty, pdf_filename, created_at 
    FROM generation_history 
    WHERE user_id = ? 
    ORDER BY created_at DESC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# 既存の関数（維持）
def save_problem(unit, topic, difficulty, problem_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO problems (unit, topic, difficulty, problem_text, solution_text, answer_key, figure_code)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (unit, topic, difficulty, problem_data.get('problem'), problem_data.get('solution'), 
          problem_data.get('answer_key'), problem_data.get('figure_code')))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database schema updated with user management tables.")
