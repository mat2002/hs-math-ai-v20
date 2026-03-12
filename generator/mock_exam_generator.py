import os
import subprocess
from jinja2 import Environment, FileSystemLoader

def generate_mock_exam_pdf(title, problems, output_filename="mock_exam.pdf"):
    """
    Jinja2テンプレートを使用して模試形式のLaTeXファイルを生成し、PDFにコンパイルする。
    """
    # テンプレート環境の設定
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'latex', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('mock_exam.tex')

    # 配点の割り振り（簡易的に均等割り）
    total_points = 100
    num_problems = len(problems)
    if num_problems > 0:
        base_points = total_points // num_problems
        remainder = total_points % num_problems
        for i, p in enumerate(problems):
            p['points'] = base_points + (1 if i < remainder else 0)

    # LaTeXソースのレンダリング
    latex_content = template.render(title=title, problems=problems)

    # 一時的なディレクトリとファイル名の設定
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    tex_path = os.path.join(output_dir, "temp_mock_exam.tex")
    pdf_path = os.path.join(output_dir, output_filename)

    # .texファイルの書き出し
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_content)

    # LaTeXコンパイル (lualatexを使用)
    try:
        for _ in range(2):
            subprocess.run(
                ["lualatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
                check=True,
                capture_output=True
            )
        
        # 中間ファイルの削除
        for ext in [".aux", ".log", ".tex"]:
            temp_file = os.path.join(output_dir, "temp_mock_exam" + ext)
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        return pdf_path
    except Exception as e:
        print(f"Error compiling mock exam LaTeX: {e}")
        return None

if __name__ == "__main__":
    # テストデータ
    test_problems = [
        {
            "problem": "2次関数 $y = x^2 - 4x + 3$ の頂点の座標を求めよ。",
            "solution": "平方完成すると $y = (x-2)^2 - 1$ となるため、頂点は $(2, -1)$ である。",
            "answer_key": "$(2, -1)$"
        },
        {
            "problem": "$\sin 30^\circ$ の値を求めよ。",
            "solution": "定義より $\sin 30^\circ = 1/2$ である。",
            "answer_key": "$1/2$"
        }
    ]
    result = generate_mock_exam_pdf("テスト模試", test_problems)
    if result:
        print(f"Mock exam PDF generated at: {result}")
    else:
        print("Failed to generate mock exam PDF.")
