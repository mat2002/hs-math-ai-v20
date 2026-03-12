import os
import yaml
from openai import OpenAI

# 環境変数からAPIキーを取得（Render等では環境変数に設定が必要）
client = OpenAI()

def generate_problem(topic, difficulty=3):
    """
    高校数学の問題を生成する
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
---
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # または適切なモデル
            messages=[
                {"role": "system", "content": "あなたは高校数学の教材作成の専門家です。正確なLaTeX数式と論理的な解説を提供します。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        # YAML部分を抽出（```yaml ... ``` で囲まれている場合を考慮）
        if "---" in content:
            yaml_content = content.split("---")[1]
        else:
            yaml_content = content.replace("```yaml", "").replace("```", "")
            
        data = yaml.safe_load(yaml_content)
        return data
    except Exception as e:
        print(f"Error generating problem: {e}")
        return None

if __name__ == "__main__":
    # テスト実行
    result = generate_problem("2次関数の最大・最小", difficulty=3)
    print(yaml.dump(result, allow_unicode=True))
