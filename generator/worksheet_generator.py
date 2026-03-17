import os
import shutil
from jinja2 import Environment, FileSystemLoader
from generator.pdf_engine import compile_latex_to_pdf

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
        
    # PDF生成エンジンを使用してコンパイル
    pdf_path = compile_latex_to_pdf(latex_content, output_filename, output_dir)

    if pdf_path:

        return pdf_path
    else:
        print(f"Error: PDF generation failed for {tex_path}")
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
    result = generate_worksheet_pdf("テスト演習プリント", test_problems, "test_worksheet.pdf")
    if result:
        print(f"PDF generated at: {result}")
    else:
        print("Failed to generate PDF.")
