import re
from ai.client import client
from ai.model_config import get_model_config

def analyze_latex_log_and_suggest_fix(latex_content: str, log_content: str) -> str:
    """
    LaTeXのコンパイルログを解析し、AIに修正案を生成させる。
    """
    model_name, params = get_model_config("latex_fixer")

    prompt = f"""
以下のLaTeXコードのコンパイルログを分析し、エラーを修正するためのLaTeXコードの修正案を提案してください。
修正は、元のLaTeXコードの該当箇所を直接修正する形式で提供してください。
修正箇所のみを抽出し、それ以外の部分は変更しないでください。

--- LaTeXコード ---
{latex_content}

--- コンパイルログ ---
{log_content}

--- 修正案 (修正されたLaTeXコードの該当部分のみ) ---
"""

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "あなたはLaTeXのエキスパートであり、コンパイルエラーを正確に特定し、修正案を提案できます。"},
                {"role": "user", "content": prompt}
            ],
            **params
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling AI for LaTeX fix: {e}")
        return ""

def apply_fix_to_latex(original_latex: str, fix_suggestion: str) -> str:
    """
    AIからの修正案を元のLaTeXコードに適用する。
    この関数は、AIが提供する修正案が元のコードの特定の部分を置き換えることを想定している。
    より高度な適用ロジックが必要になる場合がある。
    現状は、AIが提供する修正案がそのまま置き換え可能であると仮定する。
    """
    # AIが提供する修正案が、元のコードのどの部分を修正したのかを特定するのは難しい場合がある。
    # ここでは簡易的に、AIが提供する修正案が、元のコードの特定のエラー箇所を直接置き換える
    # 形式で返されることを期待する。
    # 例えば、AIが「\begin{document}」を「\documentclass{article}\begin{document}」に修正する
    # と提案した場合、その文字列をそのまま置き換える。
    # 実際には、より複雑な差分解析やパッチ適用ロジックが必要になる可能性がある。
    # 現状では、AIが提供する修正案をそのまま返すことで、呼び出し元で適切な処理を行うことを想定する。
    # 例として、AIが「修正後の完全なコード」を返す場合、それをそのまま利用する。
    # あるいは、AIが「行番号XのYをZに修正」のような指示を出す場合、それをパースして適用する。
    # ここでは、AIが修正された小さなスニペットを返すことを想定し、それを元のコードに統合する。
    # これは非常に単純な実装であり、AIの出力形式に強く依存する。

    # より堅牢な実装としては、AIに修正対象の行番号や正規表現を返させ、それに基づいて置換を行う。
    # 例: AIが "replace line X with 'new content'" のような形式で返す場合。
    # 現状は、AIが修正後のスニペットを返すことを想定し、それを元のコードに統合する。
    # この関数は、AIの出力形式に合わせて調整が必要。

    # ここでは、AIが「元のコードのこの部分をこう修正すべき」という具体的な修正スニペットを返すことを想定。
    # そのため、AIの出力が直接適用可能な形式であると仮定し、一旦ログに表示するに留める。
    # 実際の適用は、AIの出力形式が確定してから実装する。
    print("Applying AI fix suggestion (placeholder):\n" + fix_suggestion)
    # 現状はAIの修正案をそのまま返す（これは実際の修正ではない）
    # 実際の修正ロジックは、AIの出力形式に依存するため、ここではダミーとする。
    # 例: AIが `original_text -> corrected_text` の形式で返す場合
    # original_text_match = re.search(r"```latex\n(.*?)\n```\s*->\s*```latex\n(.*?)\n```", fix_suggestion, re.DOTALL)
    # if original_text_match:
    #     original_part = original_text_match.group(1)
    #     corrected_part = original_text_match.group(2)
    #     return original_latex.replace(original_part, corrected_part, 1)
    
    # AIが修正後の完全なLaTeXコードを返す場合
    # return fix_suggestion

    # 一旦、AIの修正案を元のLaTeXコードに直接適用する（AIが完全な修正済みコードを返す前提）
    # この動作は、AIの出力形式に依存するため、注意が必要。
    return fix_suggestion # AIが完全な修正済みコードを返す場合

