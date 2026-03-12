import os
import sys
import random
import sqlite3
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.problem_generator import generate_problem
from ai.textbook_writer import write_textbook_chapter
from generator.worksheet_generator import generate_worksheet_pdf
from generator.textbook_generator import generate_textbook_pdf
from generator.mock_exam_generator import generate_mock_exam_pdf
from database.schema import init_db, create_user, verify_user, save_generation_history, get_user_history, DB_PATH
from web.auth import get_user_by_id, get_user_by_username

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# データベース初期化
init_db()

# Flask-Login 設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_id = verify_user(username, password)
        if user_id:
            user = get_user_by_id(user_id)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('ユーザー名またはパスワードが正しくありません。')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if create_user(username, password, email):
            flash('登録が完了しました。ログインしてください。')
            return redirect(url_for('login'))
        else:
            flash('そのユーザー名は既に使用されています。')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/history')
@login_required
def history():
    user_history = get_user_history(current_user.id)
    return render_template('history.html', history=user_history)

@app.route('/download_history/<int:history_id>')
@login_required
def download_history(history_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT pdf_filename FROM generation_history WHERE id = ? AND user_id = ?', 
                   (history_id, current_user.id))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', row[0])
        if os.path.exists(pdf_path):
            return send_file(pdf_path, as_attachment=True)
    
    flash('ファイルが見つかりません。')
    return redirect(url_for('history'))

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    unit = request.form.get('unit')
    difficulty = int(request.form.get('difficulty', 3))
    num_problems = int(request.form.get('num_problems', 5))
    doc_type = request.form.get('type', 'worksheet')

    if doc_type == 'textbook':
        chapter_data = write_textbook_chapter(unit)
        if not chapter_data:
            return "教科書の執筆に失敗しました。", 500
        title = f"高校数学 教科書: {unit}"
        output_filename = f"textbook_{unit}_{random.randint(1000,9999)}.pdf"
        pdf_path = generate_textbook_pdf(title, [chapter_data], output_filename)
    
    elif doc_type == 'mock_exam':
        all_topics = ["数と式", "2次関数", "図形と計量", "データの分析", "場合の数と確率", "図形の性質", "整数の性質"]
        problems = []
        for _ in range(num_problems):
            current_topic = random.choice([unit, random.choice(all_topics)])
            p = generate_problem(current_topic, difficulty)
            if p: problems.append(p)
        if not problems: return "問題の生成に失敗しました。", 500
        title = f"高校数学 模擬試験 (難易度:{difficulty})"
        output_filename = f"mock_exam_{unit}_{random.randint(1000,9999)}.pdf"
        pdf_path = generate_mock_exam_pdf(title, problems, output_filename)

    else:
        problems = []
        for _ in range(num_problems):
            p = generate_problem(unit, difficulty)
            if p: problems.append(p)
        if not problems: return "問題の生成に失敗しました。", 500
        title = f"{unit} {'小テスト' if doc_type == 'exam' else '演習プリント'} (難易度:{difficulty})"
        output_filename = f"{doc_type}_{unit}_{random.randint(1000,9999)}.pdf"
        pdf_path = generate_worksheet_pdf(title, problems, output_filename)

    if pdf_path and os.path.exists(pdf_path):
        # 生成履歴を保存
        save_generation_history(current_user.id, doc_type, unit, difficulty, output_filename)
        
        response = send_file(pdf_path, as_attachment=True)
        response.headers["Content-Disposition"] = f"attachment; filename={output_filename}"
        return response
    else:
        return "PDFの生成に失敗しました。", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
