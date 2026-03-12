import os
import subprocess
from jinja2 import Environment, FileSystemLoader

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
        
    tex_path = os.path.join(output_dir, "temp_textbook.tex")
    pdf_path = os.path.join(output_dir, output_filename)

    # .texファイルの書き出し
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_content)

    # LaTeXコンパイル (lualatexを使用)
    try:
        # 目次作成のため、3回実行
        for _ in range(3):
            subprocess.run(
                ["lualatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
                check=True,
                capture_output=True
            )
        
        # 中間ファイルの削除
        for ext in [".aux", ".log", ".tex", ".toc"]:
            temp_file = os.path.join(output_dir, "temp_textbook" + ext)
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        return pdf_path
    except Exception as e:
        print(f"Error compiling textbook LaTeX: {e}")
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
    result = generate_textbook_pdf("テスト教科書", test_chapters)
    if result:
        print(f"Textbook PDF generated at: {result}")
    else:
        print("Failed to generate textbook PDF.")
