import os
import subprocess
import shutil

def compile_latex_to_pdf(latex_file_path, output_dir):
    """
    LaTeXファイルをコンパイルしてPDFを生成する。
    ローカルのTeX Live環境（uplatex + dvipdfmx）を使用する。
    """
    base_name = os.path.splitext(os.path.basename(latex_file_path))[0]
    
    # uplatex で DVI を生成
    # Windows環境での日本語ファイル名による文字化けを避けるため、作業ディレクトリを移動して実行
    cwd = os.getcwd()
    os.chdir(output_dir)
    try:
        # ファイル名のみを渡す
        target_tex = os.path.basename(latex_file_path)
        subprocess.run(
            ["uplatex", "-interaction=nonstopmode", target_tex],
            check=True, capture_output=True, text=True, encoding='utf-8'
        )
    except subprocess.CalledProcessError as e:
        print(f"uplatex compilation failed for {latex_file_path}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        os.chdir(cwd)
        return None
    finally:
        os.chdir(cwd)

    dvi_file_path = os.path.join(output_dir, f"{base_name}.dvi")
    if not os.path.exists(dvi_file_path):
        print(f"Error: DVI file not found after uplatex compilation: {dvi_file_path}")
        return None

    # dvipdfmx で PDF を生成
    os.chdir(output_dir)
    try:
        target_dvi = f"{base_name}.dvi"
        subprocess.run(
            ["dvipdfmx", target_dvi],
            check=True, capture_output=True, text=True, encoding='utf-8'
        )
    except subprocess.CalledProcessError as e:
        print(f"dvipdfmx compilation failed for {dvi_file_path}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        os.chdir(cwd)
        return None
    finally:
        os.chdir(cwd)

    pdf_file_path = os.path.join(output_dir, f"{base_name}.pdf")
    if os.path.exists(pdf_file_path):
        return pdf_file_path
    else:
        print(f"Error: PDF file not found after dvipdfmx compilation: {pdf_file_path}")
        return None


if __name__ == "__main__":
    # テスト用のLaTeXファイルを作成
    test_latex_content = r"""
    \documentclass[uplatex,dvipdfmx]{jsarticle}
    \usepackage{amsmath}
    \usepackage{tikz}
    \begin{document}
    こんにちは、世界！
    
    $x^2 + y^2 = z^2$
    
    \begin{tikzpicture}
    \draw (0,0) circle (1cm);
    \end{tikzpicture}
    
    \end{document}
    """
    
    test_dir = "./test_output"
    os.makedirs(test_dir, exist_ok=True)
    test_tex_path = os.path.join(test_dir, "test.tex")
    
    with open(test_tex_path, "w", encoding="utf-8") as f:
        f.write(test_latex_content)
        
    print(f"Test LaTeX file created at {test_tex_path}")
    
    pdf_path = compile_latex_to_pdf(test_tex_path, test_dir)
    
    if pdf_path:
        print(f"PDF generated successfully at {pdf_path}")
    else:
        print("PDF generation failed.")

    # クリーンアップ
    # shutil.rmtree(test_dir)
    # print(f"Cleaned up {test_dir}")
