import os
import yaml
import random
import re
from ai.client import client
from ai.tikz_generator import generate_tikz_code
from ai.model_config import get_model_config
from ai.exam_reproduction import build_exam_reproduction_prompt

def escape_latex_special_chars(text):
    """
    LaTeXの特殊文字をエスケープする。数式モード内はエスケープしない。
    """
    # LaTeXの特殊文字とエスケープシーケンスのマップ
    # バックスラッシュは他のエスケープと競合しないように最後に処理する
    latex_special_chars = {
        # '&' は tabular 環境などで使われるため、地の文ではエスケープ
        # '%' はコメントアウト文字なので、地の文ではエスケープ
        # '#' はコマンド定義などで使われるため、地の文ではエスケープ
        # '_' は下付き文字なので、地の文ではエスケープ
        # '{' と '}' はグループ化に使われるため、地の文ではエスケープ
        # '~' は非改行スペースなので、地の文ではエスケープ
        # '^' は上付き文字なので、地の文ではエスケープ
        # '<' と '>' は比較演算子などで使われるが、地の文ではエスケープ
        # バックスラッシュ自体もエスケープ
        '&': '\\&',
        '%': '\\%',
        '#': '\\#',
        '_': '\\_',
        '{': '\\{',
        '}': '\\}',
        '~': '\\textasciitilde{}',
        '^': '\\textasciicircum{}',
        '<': '\\textless{}',
        '>': '\\textgreater{}',
    }

    # 数式モード ($...$ または $$...$$) を見つけて、それ以外の部分をエスケープする
    # $...$ または $$...$$ のパターンをキャプチャグループとして含む
    # re.split を使うと、区切り文字も結果に含まれるため、処理がしやすい
    # 正規表現を修正: LaTeXの数式モードの開始/終了を示す `$` と `$$` を正しくマッチさせる
    # Pythonの正規表現では、`$` は行末を示す特殊文字なので、リテラルとしてマッチさせるには `\$` とエスケープする必要がある。
    # ただし、Pythonの文字列リテラル内で `\` を表現するには `\\` と書く必要があるため、`\\$` となる。
    # `$$` の場合は `\\$\$` となる。
    # ここでは、より堅牢な数式モードの検出のために、生の `$` と `$$` を使用し、
    # それらがLaTeXコマンドの一部ではないことを前提とする。
    # ただし、`re.split` の引数に渡す文字列リテラル内では `\` もエスケープが必要なので `\\` となる。
    # したがって、`(\\$[^\\]*?\\$|\\\$[^\\]*?\\\$)` が正しい。
    # しかし、これだと `\(` や `\)` のようなLaTeXコマンド内のドル記号を誤って解釈する可能性がある。
    # そこで、より単純に `$` と `$$` を区切り文字として扱い、数式モードの開始と終了を区別する。
    # このアプローチでは、数式モードの開始と終了が正しくペアになっていることを前提とする。
    
    # 数式モードの正規表現: `$` で囲まれた部分、または `$$` で囲まれた部分
    # `re.split` は区切り文字もリストに含めるため、数式部分と地の文部分を交互に取得できる
    # raw文字列リテラル `r` を使用し、`$` を `\$` でエスケープする
    parts = re.split(r'(\$[^$]*?\$|\$\$[^$]*?\$\$)', text)
    
    escaped_text = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # 数式モードの部分はそのまま
            escaped_text.append(part)
        else:  # 数式モード以外の部分をエスケープ
            # ここで、エスケープが必要な文字を置換
            for char, escaped_char in latex_special_chars.items():
                part = part.replace(char, escaped_char)
            # バックスラッシュは他のエスケープ処理と競合しないように最後に処理
            part = part.replace('\\', '\\textbackslash{}')
            escaped_text.append(part)
            
    return ''.join(escaped_text)

def generate_problem(topic, difficulty=3, include_figure=True, exam_type="standard", target_exam=None):
    """
    高校数学の問題を生成する。
    exam_type: "standard", "common_test", "hard", "reproduction" (入試再現)
    target_exam: "東京大学", "京都大学" など (exam_type="reproduction" の場合)
    """
    model_name, params = get_model_config("problem_gen")
    
    if exam_type == "reproduction" and target_exam:
        prompt = build_exam_reproduction_prompt(target_exam, topic)
    else:
        # 従来のプロンプト構築
        exam_context = {
            "standard": "教科書の章末問題レベルの標準的な問題を作成してください。",
            "common_test": "大学入学共通テスト形式で、太郎さんと花子さんの会話や、日常生活の事象を数学的にモデル化する問題を含めてください。誘導形式（穴埋め）を意識した構成にしてください。",
            "hard": "難関国立大学の二次試験レベルの問題を作成してください。複数の分野を融合させ、高い思考力を要求する記述式問題にしてください。"
        }
        
        prompt = f"""
高校数学の問題を作成してください。

単元・トピック: {topic}
難易度: {difficulty} (1:基礎, 3:標準, 5:発展)
形式: {exam_context.get(exam_type, exam_context["standard"])}

※単元・トピックが「数学C」の場合、以下の内容を考慮してください。
  - 平面上のベクトル、空間のベクトル、複素数平面、2次曲線（放物線、楕円、双曲線）などが含まれます。
  - これらの概念を適切に組み合わせて問題を作成してください。

【思考プロセス】
1. まず、この単元と難易度にふさわしい数学的概念を特定してください。
2. 次に、その概念を用いた具体的な数値を設定し、解がきれいになるように調整してください。
3. 最後に、問題文、解答、解説をLaTeX形式で構成してください。

出力形式は以下のYAML形式のみとしてください。余計な解説文は含めないでください。
**重要**: YAMLの文字列内でバックスラッシュ `\` を使用する場合は、必ず二重にエスケープ `\\` するか、またはリテラルスタイル `|` を使用してください。特に `answer_key` はLaTeX形式ではなく、プレーンテキストで記述してください。また、LaTeXの特殊文字（`%`, `_`, `&`, `#`, `{`, `}`, `~`, `^`, `<`, `>`, `\\`）は、数式モードの外では必ずエスケープしてください。

---
problem: |
  (問題文をLaTeX形式で記述してください。数式は $...$ または $$...$$ で囲んでください)
solution: |
  (解答と解説をLaTeX形式で記述してください。解法の手順を論理的に説明してください)
difficulty: {difficulty}
answer_key: (最終的な答えのみをプレーンテキストで簡潔に記述してください。LaTeX形式は使用しないでください)
needs_figure: (図解が必要な場合は true、不要な場合は false)
exam_type: "{exam_type}"
---
"""
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "あなたは高校数学の教材作成の専門家です。正確なLaTeX数式と論理的な解説を提供します。"},
                {"role": "user", "content": prompt}
            ],
            **params
        )
        
        content = response.choices[0].message.content
        
        # YAMLパースエラーを回避するための堅牢な抽出処理
        data = {}
        
        # 1. problem の抽出
        problem_match = re.search(r'problem:\s*\|\s*\n(.*?)(?=\n\w+:|---|$)', content, re.DOTALL)
        if problem_match:
            data['problem'] = escape_latex_special_chars(problem_match.group(1).strip())
        
        # 2. solution の抽出
        solution_match = re.search(r'solution:\s*\|\s*\n(.*?)(?=\n\w+:|---|$)', content, re.DOTALL)
        if solution_match:
            data['solution'] = escape_latex_special_chars(solution_match.group(1).strip())
            
        # 3. answer_key の抽出 (YAMLパースに頼らず正規表現で直接抽出)
        # answer_key は単一行で、次のキーまたは --- または行末までをキャプチャ
        answer_key_match = re.search(r'answer_key:\s*(.*?)(?=\n(?:\w+:|---|$))', content)
        if answer_key_match:
            data['answer_key'] = escape_latex_special_chars(answer_key_match.group(1).strip())
        
        # 4. その他のフィールドをYAMLとしてパース（フォールバック）
        # problem, solution, answer_key は正規表現で優先的に抽出するため、ここでは上書きしない
        try:
            # YAMLブロック全体を抽出
            yaml_block_match = re.search(r'---\s*\n(.*?)\n---\s*', content, re.DOTALL)
            if yaml_block_match:
                yaml_content = yaml_block_match.group(1)
            else:
                # --- で囲まれていない場合も考慮
                yaml_content = content.replace("```yaml", "").replace("```", "")
            
            yaml_data = yaml.safe_load(yaml_content)
            if isinstance(yaml_data, dict):
                for key in ['difficulty', 'needs_figure', 'exam_type']:
                    if key in yaml_data:
                        data[key] = yaml_data[key]
        except Exception as ye:
            print(f"YAML fallback parsing error: {ye}")
            # YAMLパースに失敗しても、正規表現で抽出できていれば続行
            if 'problem' not in data:
                raise ValueError(f"AI生成データのパースに失敗しました: {ye}")

        # デフォルト値の設定
        data.setdefault('difficulty', difficulty)
        data.setdefault('needs_figure', False)
        data.setdefault('exam_type', exam_type)
        
        # 図の生成が必要な場合
        if include_figure and data.get("needs_figure"):
            tikz_code = generate_tikz_code(topic, data.get("problem", ""))
            if tikz_code:
                data["figure_code"] = tikz_code
                
        return data
    except Exception as e:
        print(f"Error generating problem: {e}")
        return None
