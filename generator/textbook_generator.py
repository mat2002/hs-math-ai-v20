import os
import shutil
from jinja2 import Environment, FileSystemLoader
from generator.pdf_engine import compile_latex_to_pdf

def generate_textbook_pdf(title, chapters, output_filename="textbook.pdf"):
    """
    Jinja2テンプレートを使用して教科書のLaTeXファイルを生成し、PDFにコンパイルする。
    """
    # テンプレート環境の設定
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'latex', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('textbook.tex')

    # LaTeXソースのレンダリング
    latex_content = template.render(title=title, chapters=chapters)

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
    test_chapters = [
        {
            "title": "2次関数",
            "sections": [
                {
                    "title": "2次関数の定義",
                    "content": "\\begin{definitionbox}{2次関数}\n$y = ax^2 + bx + c$ ($a \\neq 0$) の形で表される関数を2次関数という。\n\\end{definitionbox}",
                    "figure_code": "\\begin{tikzpicture}\\draw[->](-2,0)--(2,0);\\draw[->](0,-1)--(0,3);\\draw[domain=-1.5:1.5] plot(\\x,{\\x*\\x});\\end{tikzpicture}"
                }
            ]
        }
    ]
    result = generate_textbook_pdf("テスト教科書", test_chapters, "test_textbook.pdf")
    if result:
        print(f"Textbook PDF generated at: {result}")
    else:
        print("Failed to generate textbook PDF.")
