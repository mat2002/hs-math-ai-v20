import os
import subprocess
from jinja2 import Environment, FileSystemLoader

def generate_worksheet_pdf(title, problems, output_filename="worksheet.pdf"):
    """
    Jinja2テンプレートを使用してLaTeXファイルを生成し、PDFにコンパイルする。
    """
    # テンプレート環境の設定
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'latex', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('worksheet.tex')

    # LaTeXソースのレンダリング
    latex_content = template.render(title=title, problems=problems)

    # 一時的なディレクトリとファイル名の設定
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    tex_path = os.path.join(output_dir, "temp_worksheet.tex")
    pdf_path = os.path.join(output_dir, output_filename)

    # .texファイルの書き出し
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_content)

    # LaTeXコンパイル (lualatexを使用)
    # Render環境ではTeX Liveがインストールされている必要があります
    try:
        # 2回実行して相互参照を解決
        for _ in range(2):
            subprocess.run(
                ["lualatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
                check=True,
                capture_output=True
            )
        
        # 中間ファイルの削除
        for ext in [".aux", ".log", ".tex"]:
            temp_file = os.path.join(output_dir, "temp_worksheet" + ext)
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        return pdf_path
    except Exception as e:
        print(f"Error compiling LaTeX: {e}")
        return None

if __name__ == "__main__":
    # テストデータ
    test_problems = [
        {
            "problem": "$2x^2 - 4x + 1 = 0$ の解を求めよ。",
            "solution": "解の公式より $x = \\frac{2 \\pm \\sqrt{2}}{2}$ となる。",
            "answer_key": "$x = \\frac{2 \\pm \\sqrt{2}}{2}$"
        }
    ]
    result = generate_worksheet_pdf("テスト演習プリント", test_problems)
    if result:
        print(f"PDF generated at: {result}")
    else:
        print("Failed to generate PDF.")
