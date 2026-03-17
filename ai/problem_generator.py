import os
import yaml
import random
import re
from ai.client import client
from ai.model_config import get_model_config
from ai.exam_reproduction import build_exam_reproduction_prompt
from generator.latex_validator import validate_latex
from ai.math_engine import generate_latex_from_sympy

FIGURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'latex', 'figures')

def get_figure_code(figure_id: str) -> str:
    """
    指定されたfigure_idに対応するTikZコードをファイルから読み込む。
    """
    figure_path = os.path.join(FIGURES_DIR, f"{figure_id}.tex")
    if os.path.exists(figure_path):
        with open(figure_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f"Warning: Figure ID '{figure_id}' not found. Returning placeholder.")
        return f"\\begin{{center}}\n  [Figure not found: {figure_id}]\n\\end{{center}}"


def process_ai_output(text: str) -> str:
    """
    AIの出力テキスト（SymPy形式の数式を含む）を処理し、
    完全なLaTeXコードに変換する。
    """
    # <sympy>...</sympy> タグを見つけて、中の式をLaTeXに変換する
    def replace_sympy(match):
        sympy_expr = match.group(1).strip()
        latex_code = generate_latex_from_sympy(sympy_expr)
        # インライン数式として扱う
        return f"${latex_code}$"

    # 正規表現で <sympy> タグを検索し、replace_sympy関数で置換
    processed_text = re.sub(r"<sympy>(.*?)</sympy>", replace_sympy, text)
    return processed_text

def generate_problem(topic, difficulty=3, include_figure=True, exam_type="standard", target_exam=None):
    """
    高校数学の問題を生成する。
    AIにはLaTeXを直接生成させず、構造化されたテキストとSymPy形式の数式を生成させる。
    """
    model_name, params = get_model_config("problem_gen_structured")

    # TODO: exam_type に応じたプロンプトの分岐を後で実装

    prompt = f"""
高校数学の問題の構成要素をYAML形式で出力してください。

単元・トピック: {topic}
難易度: {difficulty} (1:基礎, 3:標準, 5:発展)

【重要】
LaTeXを直接記述しないでください。
すべての数式は、<sympy>...</sympy> タグで囲んだSymPy形式の文字列として記述してください。
例: 「xの2乗は <sympy>x**2</sympy> です。」
図が必要な場合は、その図の内容を示すfigure_idを指定してください。

出力形式は以下のYAML形式のみとします。余計な解説文は含めないでください。
---
problem_text: |
  (問題文を、数式部分を<sympy>タグで囲んで記述)
solution_text: |
  (解答と解説を、数式部分を<sympy>タグで囲んで記述)
figure_id: (図のIDを文字列で指定、不要な場合は "none")
difficulty: {difficulty}
answer_key: (最終的な答えのみをプレーンテキストで簡潔に記述)
exam_type: "{exam_type}"
---
"""

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "あなたは高校数学の教材設計の専門家です。問題文、解説、数式、図の構成要素を構造化して出力します。"},
                {"role": "user", "content": prompt}
            ],
            **params
        )

        content = response.choices[0].message.content
        yaml_content = content.replace("```yaml", "").replace("```", "").strip()
        
        # --- で囲まれている場合、その中身だけを抽出
        yaml_block_match = re.search(r'---\s*\n(.*?)\n---\s*', yaml_content, re.DOTALL)
        if yaml_block_match:
            yaml_content = yaml_block_match.group(1)

        data = yaml.safe_load(yaml_content)

        # AIの出力を処理してLaTeXコードを生成
        problem_latex = process_ai_output(data.get("problem_text", ""))
        solution_latex = process_ai_output(data.get("solution_text", ""))

        # 生成されたLaTeXコードを検証
        if not validate_latex(problem_latex) or not validate_latex(solution_latex):
            # TODO: フェーズ5で自動修正ロジックを実装
            raise ValueError("Generated LaTeX code failed validation.")

        # 最終的なデータ構造を構築
        final_data = {
            "problem": problem_latex,
            "solution": solution_latex,
            "difficulty": data.get("difficulty", difficulty),
            "answer_key": data.get("answer_key", ""),
            "exam_type": data.get("exam_type", exam_type),
            "figure_id": data.get("figure_id", "none")
        }
        
        # フェーズ4: figure_idに基づいて図のコードを挿入
        if final_data["figure_id"] != "none":
            final_data["figure_code"] = get_figure_code(final_data["figure_id"])

        return final_data

    except Exception as e:
        print(f"Error generating structured problem: {e}")
        return None
