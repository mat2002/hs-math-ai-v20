import os
import yaml
from openai import OpenAI
from ai.tikz_generator import generate_tikz_code

client = OpenAI()

def generate_problem(topic, difficulty=3, include_figure=True):
    """
    高校数学の問題を生成し、必要に応じてTikZ図も生成する。
    """
    prompt = f"""
高校数学の問題を作成してください。

単元: {topic}
難易度: {difficulty} (1:基礎, 3:標準, 5:発展)

出力形式は以下のYAML形式のみとしてください。余計な解説文は含めないでください。

---
problem: |
  (問題文をLaTeX形式で記述してください。数式は $...$ または $$...$$ で囲んでください)
solution: |
  (解答と解説をLaTeX形式で記述してください)
difficulty: {difficulty}
answer_key: (最終的な答えのみを簡潔に記述してください)
needs_figure: (図解が必要な場合は true、不要な場合は false)
---
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは高校数学の教材作成の専門家です。正確なLaTeX数式と論理的な解説を提供します。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        if "---" in content:
            yaml_content = content.split("---")[1]
        else:
            yaml_content = content.replace("```yaml", "").replace("```", "")
            
        data = yaml.safe_load(yaml_content)
        
        # 図の生成が必要な場合
        if include_figure and data.get("needs_figure"):
            tikz_code = generate_tikz_code(topic, data.get("problem", ""))
            if tikz_code:
                data["figure_code"] = tikz_code
                
        return data
    except Exception as e:
        print(f"Error generating problem: {e}")
        return None

if __name__ == "__main__":
    # テスト実行
    result = generate_problem("2次関数の最大・最小", difficulty=3)
    print(yaml.dump(result, allow_unicode=True))
