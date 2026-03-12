import os
import sys
from flask import Flask, render_template, request, send_file, redirect, url_for

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.problem_generator import generate_problem
from generator.worksheet_generator import generate_worksheet_pdf

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

    # 問題の生成
    problems = []
    for _ in range(num_problems):
        p = generate_problem(unit, difficulty)
        if p:
            problems.append(p)
    
    if not problems:
        return "問題の生成に失敗しました。APIキーの設定を確認してください。", 500

    # PDFの生成
    title = f"{unit} 演習プリント (難易度:{difficulty})"
    output_filename = f"{doc_type}_{unit}.pdf"
    pdf_path = generate_worksheet_pdf(title, problems, output_filename)

    if pdf_path and os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return "PDFの生成に失敗しました。サーバーのLaTeX環境を確認してください。", 500

if __name__ == '__main__':
    # 外部からのアクセスを許可するため 0.0.0.0 で起動
    app.run(host='0.0.0.0', port=5000)
