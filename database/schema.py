import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'problems.db')

def init_db():
    """
    データベースとテーブルを初期化する。
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 問題テーブルの作成
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
    
    # 検索を高速化するためのインデックス
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_unit_topic ON problems(unit, topic)')
    
    conn.commit()
    conn.close()

def save_problem(unit, topic, difficulty, problem_data):
    """
    生成された問題をデータベースに保存する。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO problems (unit, topic, difficulty, problem_text, solution_text, answer_key, figure_code)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        unit,
        topic,
        difficulty,
        problem_data.get('problem'),
        problem_data.get('solution'),
        problem_data.get('answer_key'),
        problem_data.get('figure_code')
    ))
    
    conn.commit()
    conn.close()

def get_random_problems(unit, topic, difficulty, limit=5):
    """
    条件に合う問題をランダムに取得する。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT problem_text, solution_text, answer_key, figure_code 
    FROM problems 
    WHERE unit = ? AND topic = ? AND difficulty = ?
    ORDER BY RANDOM() LIMIT ?
    ''', (unit, topic, difficulty, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "problem": row[0],
            "solution": row[1],
            "answer_key": row[2],
            "figure_code": row[3]
        } for row in rows
    ]

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
