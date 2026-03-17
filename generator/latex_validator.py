import re

def validate_latex(text: str) -> bool:
    """
    LaTeXコードの基本的な構文を検証します。
    数式の閉じ忘れなどをチェックします。
    """
    # 数式環境の閉じ忘れチェック
    if text.count(r"\[") != text.count(r"\]"):
        print(r"LaTeX Validation Error: Mismatched \[ and \] environments.")
        return False

    if text.count("$") % 2 != 0:
        print("LaTeX Validation Error: Mismatched $ for inline math.")
        return False

    # begin-end環境の基本的な整合性チェック (簡易版)
    # より厳密なチェックにはAST解析などが必要だが、ここでは簡易的に
    environments = [
        "document", "problem", "solution", "align", "equation", "figure", "table",
        "itemize", "enumerate", "description", "tikzpicture"
    ]
    for env in environments:
        if text.count(f"\\begin{{{env}}}") != text.count(f"\\end{{{env}}}"):
            print(f"LaTeX Validation Error: Mismatched \\begin{{{env}}} and \\end{{{env}}} environments.")
            return False

    return True

def validate_tikz(code: str) -> bool:
    """
    TikZコードの基本的な構文を検証します。
    """
    if "\\begin{tikzpicture}" not in code:
        print("TikZ Validation Error: Missing \\begin{tikzpicture}.")
        return False

    if "\\end{tikzpicture}" not in code:
        print("TikZ Validation Error: Missing \\end{tikzpicture}.")
        return False

    return True

if __name__ == '__main__':
    # テストケース
    print("--- LaTeX Validation Tests ---")
    valid_latex = r"This is $a+b$ math. \[ x^2 \] And some text."
    invalid_latex_dollar = r"This is $a+b$ math. \[ x^2 \] And some text $"
    invalid_latex_bracket = r"This is $a+b$ math. \[ x^2 And some text."
    invalid_latex_env = r"\begin{document} Hello \end{document} \begin{problem} Problem."

    print(f"Valid LaTeX: {validate_latex(valid_latex)}") # Expected: True
    print(f"Invalid LaTeX (dollar): {validate_latex(invalid_latex_dollar)}") # Expected: False
    print(f"Invalid LaTeX (bracket): {validate_latex(invalid_latex_bracket)}") # Expected: False
    print(f"Invalid LaTeX (environment): {validate_latex(invalid_latex_env)}") # Expected: False

    print("\n--- TikZ Validation Tests ---")
    valid_tikz = r"\begin{tikzpicture}\draw (0,0) -- (1,1);\end{tikzpicture}"
    invalid_tikz_begin = r"\draw (0,0) -- (1,1);\end{tikzpicture}"
    invalid_tikz_end = r"\begin{tikzpicture}\draw (0,0) -- (1,1);"

    print(f"Valid TikZ: {validate_tikz(valid_tikz)}") # Expected: True
    print(f"Invalid TikZ (missing begin): {validate_tikz(invalid_tikz_begin)}") # Expected: False
    print(f"Invalid TikZ (missing end): {validate_tikz(invalid_tikz_end)}") # Expected: False
