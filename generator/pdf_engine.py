import os
import subprocess
import shutil
import time
import tempfile
from ai.latex_fixer import analyze_latex_log_and_suggest_fix, apply_fix_to_latex

def compile_latex_to_pdf(latex_content: str, output_filename: str, output_dir: str, max_retries: int = 3):
    """
    LaTeXファイルをコンパイルしてPDFを生成する。
    ローカルのTeX Live環境（uplatex + dvipdfmx）を使用する。
    """
    base_name = os.path.splitext(output_filename)[0]
    full_pdf_path = os.path.join(output_dir, output_filename)
    final_tex_path = os.path.join(output_dir, f"{base_name}.tex")

    current_latex_content = latex_content

    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}/{max_retries} to compile LaTeX...")
        
        # 一時ファイルにLaTeXコンテンツを書き込む
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tex', encoding='utf-8', dir=output_dir) as tmp_tex_file:
            tmp_tex_file.write(current_latex_content)
            tmp_tex_path = tmp_tex_file.name
        
        tmp_base_name = os.path.splitext(os.path.basename(tmp_tex_path))[0]
        
        # uplatex で DVI を生成
        uplatex_log = ""
        try:
            uplatex_proc = subprocess.run(
                ["uplatex", "-interaction=nonstopmode", tmp_tex_path],
                check=False, capture_output=True, text=True, encoding=\'utf-8\', cwd=output_dir
            )
            uplatex_log = uplatex_proc.stdout + uplatex_proc.stderr
            if uplatex_proc.returncode != 0:
                raise subprocess.CalledProcessError(uplatex_proc.returncode, uplatex_proc.args, output=uplatex_proc.stdout, stderr=uplatex_proc.stderr)
        except subprocess.CalledProcessError as e:
            print(f"uplatex compilation failed. Attempting to fix with AI...")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            # AIに修正を依頼
            fix_suggestion = analyze_latex_log_and_suggest_fix(current_latex_content, uplatex_log)
            if fix_suggestion:
                current_latex_content = apply_fix_to_latex(current_latex_content, fix_suggestion)
                print("AI suggested a fix. Retrying...")
                os.remove(tmp_tex_path) # 一時ファイルを削除して再試行
                continue
            else:
                print("AI could not suggest a fix or returned empty. Aborting.")
                os.remove(tmp_tex_path)
                return None
        
        dvi_file_path = os.path.join(output_dir, f"{tmp_base_name}.dvi")
        if not os.path.exists(dvi_file_path):
            print(f"Error: DVI file not found after uplatex. Attempting to fix with AI...")
            fix_suggestion = analyze_latex_log_and_suggest_fix(current_latex_content, uplatex_log)
            if fix_suggestion:
                current_latex_content = apply_fix_to_latex(current_latex_content, fix_suggestion)
                print("AI suggested a fix. Retrying...")
                os.remove(tmp_tex_path)
                continue
            else:
                print("AI could not suggest a fix or returned empty. Aborting.")
                os.remove(tmp_tex_path)
                return None

        # dvipdfmx で PDF を生成
        dvipdfmx_log = ""
        try:
            dvipdfmx_proc = subprocess.run(
                ["dvipdfmx", dvi_file_path],
                check=False, capture_output=True, text=True, encoding=\'utf-8\', cwd=output_dir
            )
            dvipdfmx_log = dvipdfmx_proc.stdout + dvipdfmx_proc.stderr
            if dvipdfmx_proc.returncode != 0:
                raise subprocess.CalledProcessError(dvipdfmx_proc.returncode, dvipdfmx_proc.args, output=dvipdfmx_proc.stdout, stderr=dvipdfmx_proc.stderr)
        except subprocess.CalledProcessError as e:
            print(f"dvipdfmx compilation failed. Attempting to fix with AI...")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            fix_suggestion = analyze_latex_log_and_suggest_fix(current_latex_content, dvipdfmx_log)
            if fix_suggestion:
                current_latex_content = apply_fix_to_latex(current_latex_content, fix_suggestion)
                print("AI suggested a fix. Retrying...")
                os.remove(tmp_tex_path)
                os.remove(dvi_file_path) # DVIも削除して再試行
                continue
            else:
                print("AI could not suggest a fix or returned empty. Aborting.")
                os.remove(tmp_tex_path)
                os.remove(dvi_file_path)
                return None
        
        # PDFが正常に生成されたか確認
        if os.path.exists(os.path.join(output_dir, f"{tmp_base_name}.pdf")):
            # 成功した場合、最終的な.texファイルを保存し、一時ファイルをクリーンアップ
            with open(final_tex_path, "w", encoding="utf-8") as f:
                f.write(current_latex_content)
            
            # 生成されたPDFをリネーム
            shutil.move(os.path.join(output_dir, f"{tmp_base_name}.pdf"), full_pdf_path)
            
            # 一時ファイルをクリーンアップ
            for ext in [".aux", ".log", ".dvi", ".fls", ".idx", ".ilg", ".ind", ".lof", ".lot", ".out", ".toc", ".synctex.gz", ".fdb_latexmk"]: # 一般的な補助ファイル
                if os.path.exists(os.path.join(output_dir, f"{tmp_base_name}{ext}")):
                    os.remove(os.path.join(output_dir, f"{tmp_base_name}{ext}"))
            if os.path.exists(tmp_tex_path):
                os.remove(tmp_tex_path)

            print(f"PDF and TEX generated successfully: {full_pdf_path}")
            return full_pdf_path
        else:
            print(f"PDF file not found after dvipdfmx. Attempting to fix with AI...")
            fix_suggestion = analyze_latex_log_and_suggest_fix(current_latex_content, dvipdfmx_log)
            if fix_suggestion:
                current_latex_content = apply_fix_to_latex(current_latex_content, fix_suggestion)
                print("AI suggested a fix. Retrying...")
                os.remove(tmp_tex_path)
                if os.path.exists(dvi_file_path): os.remove(dvi_file_path)
                continue
            else:
                print("AI could not suggest a fix or returned empty. Aborting.")
                os.remove(tmp_tex_path)
                if os.path.exists(dvi_file_path): os.remove(dvi_file_path)
                return None

    print(f"Failed to compile LaTeX after {max_retries} attempts.")
    return None


if __name__ == "__main__":
    # テスト用のLaTeXコンテンツ
    test_latex_content_success = r"""
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

    test_latex_content_fail = r"""
\documentclass[uplatex,dvipdfmx]{jsarticle}
\usepackage{amsmath}
\usepackage{tikz}
\begin{document}
こんにちは、世界！

$x^2 + y^2 = z^2

\begin{tikzpicture}
\draw (0,0) circle (1cm);
\end{tikzpicture}

\end{document}
""" # 意図的に数式を閉じないエラー
    
    test_dir = "./test_output"
    os.makedirs(test_dir, exist_ok=True)

    print("\n--- Testing successful compilation ---")
    pdf_path_success = compile_latex_to_pdf(test_latex_content_success, "test_success.pdf", test_dir)
    if pdf_path_success:
        print(f"Successful PDF generated at {pdf_path_success}")
    else:
        print("Successful PDF generation failed.")

    print("\n--- Testing failed compilation with AI fix attempt ---")
    # このテストはAIの応答に依存するため、AIが適切な修正を返さないと失敗する可能性があります。
    # analyze_latex_log_and_suggest_fix と apply_fix_to_latex の実装に依存します。
    pdf_path_fail = compile_latex_to_pdf(test_latex_content_fail, "test_fail_fixed.pdf", test_dir)
    if pdf_path_fail:
        print(f"Failed PDF (fixed by AI) generated at {pdf_path_fail}")
    else:
        print("Failed PDF generation (AI fix failed).")

    # クリーンアップ
    # shutil.rmtree(test_dir)
    # print(f"Cleaned up {test_dir}")
