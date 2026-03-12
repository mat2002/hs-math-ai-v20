import os
import sys
import random
from flask import Flask, render_template, request, send_file, redirect, url_for

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.problem_generator import generate_problem
from ai.textbook_writer import write_textbook_chapter
from generator.worksheet_generator import generate_worksheet_pdf
from generator.textbook_generator import generate_textbook_pdf
from generator.mock_exam_generator import generate_mock_exam_pdf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # フォームデータの取得
    unit = request.form.get('unit')
    difficulty = int(request.form.get('difficulty', 3))
    num_problems = int(request.form.get('num_problems', 5))
    doc_type = request.form.get('type', 'worksheet')

    if doc_type == 'textbook':
        # 教科書の生成
        chapter_data = write_textbook_chapter(unit)
        if not chapter_data:
            return "教科書の執筆に失敗しました。APIキーの設定を確認してください。", 500
        
        title = f"高校数学 教科書: {unit}"
        output_filename = f"textbook_{unit}.pdf"
        pdf_path = generate_textbook_pdf(title, [chapter_data], output_filename)
    
    elif doc_type == 'mock_exam':
        # 模試形式の生成（複数単元からランダムに選定）
        all_topics = ["数と式", "2次関数", "図形と計量", "データの分析", "場合の数と確率", "図形の性質", "整数の性質"]
        problems = []
        for _ in range(num_problems):
            # 選択された単元を優先しつつ、他の単元も混ぜる
            current_topic = random.choice([unit, random.choice(all_topics)])
            p = generate_problem(current_topic, difficulty)
            if p:
                problems.append(p)
        
        if not problems:
            return "問題の生成に失敗しました。", 500

        title = f"高校数学 模擬試験 (難易度:{difficulty})"
        output_filename = f"mock_exam_{unit}.pdf"
        pdf_path = generate_mock_exam_pdf(title, problems, output_filename)

    else:
        # 演習プリント・小テストの生成
        problems = []
        for _ in range(num_problems):
            p = generate_problem(unit, difficulty)
            if p:
                problems.append(p)
        
        if not problems:
            return "問題の生成に失敗しました。APIキーの設定を確認してください。", 500

        title = f"{unit} {'小テスト' if doc_type == 'exam' else '演習プリント'} (難易度:{difficulty})"
        output_filename = f"{doc_type}_{unit}.pdf"
        pdf_path = generate_worksheet_pdf(title, problems, output_filename)

    if pdf_path and os.path.exists(pdf_path):
        # ファイル名をヘッダーに含めて返す
        response = send_file(pdf_path, as_attachment=True)
        response.headers["Content-Disposition"] = f"attachment; filename={output_filename}"
        return response
    else:
        return "PDFの生成に失敗しました。サーバーのLaTeX環境を確認してください。", 500

if __name__ == '__main__':
    # 外部からのアクセスを許可するため 0.0.0.0 で起動
    app.run(host='0.0.0.0', port=5000)
