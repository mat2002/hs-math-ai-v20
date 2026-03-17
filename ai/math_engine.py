import sympy as sp

def generate_latex_from_sympy(expression_str: str) -> str:
    """
    SymPyの式文字列を受け取り、対応するLaTeX表現を生成します。
    """
    try:
        # 式をSymPyオブジェクトとしてパース
        expr = sp.sympify(expression_str)
        # LaTeXに変換
        latex_code = sp.latex(expr)
        return latex_code
    except (sp.SympifyError, TypeError) as e:
        print(f"Error generating LaTeX from SymPy expression '{expression_str}': {e}")
        return f"\\text{{Error: Invalid expression '{expression_str}'}}"

if __name__ == '__main__':
    # テストケース
    print("--- SymPy to LaTeX Generation Tests ---")

    # 有効な式
    expr1 = "x**2 + 3*x + 1"
    latex1 = generate_latex_from_sympy(expr1)
    print(f"Expression: {expr1} -> LaTeX: {latex1}") # Expected: x^{2} + 3 x + 1

    expr2 = "sin(theta) + cos(phi)"
    latex2 = generate_latex_from_sympy(expr2)
    print(f"Expression: {expr2} -> LaTeX: {latex2}") # Expected: \sin{\theta} + \cos{\phi}

    expr3 = "Integral(x**2, x)"
    latex3 = generate_latex_from_sympy(expr3)
    print(f"Expression: {expr3} -> LaTeX: {latex3}") # Expected: \int x^{2}\, dx

    # 無効な式
    expr4 = "invalid_expression("
    latex4 = generate_latex_from_sympy(expr4)
    print(f"Expression: {expr4} -> LaTeX: {latex4}") # Expected: Error message

    expr5 = "1/0"
    latex5 = generate_latex_from_sympy(expr5)
    print(f"Expression: {expr5} -> LaTeX: {latex5}") # Expected: Error message
