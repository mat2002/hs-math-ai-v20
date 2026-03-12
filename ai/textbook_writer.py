import os
import yaml
from openai import OpenAI
from ai.tikz_generator import generate_tikz_code

client = OpenAI()

def write_textbook_chapter(topic):
    """
    指定された単元について、教科書の1章分（複数の節）を執筆する。
    """
    prompt = f"""
高校数学の教科書を執筆してください。

単元: {topic}

出力形式は以下のYAML形式のみとしてください。余計な解説文は含めないでください。

---
title: "{topic}"
sections:
  - title: "導入と定義"
    content: |
      (定義や基本的な概念の解説をLaTeX形式で記述してください。
      definitionbox環境を使用して定義を囲んでください。)
  - title: "定理と性質"
    content: |
      (定理の紹介と証明、性質の解説をLaTeX形式で記述してください。
      theorembox環境を使用して定理を囲んでください。)
  - title: "例題と解法"
    content: |
      (具体的な例題とその解法をLaTeX形式で記述してください。
      examplebox環境を使用して例題を囲んでください。)
---
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは高校数学の教科書執筆の専門家です。正確で論理的な解説を提供します。"},
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
        
        # 各節に対して図が必要か判断し、生成する（簡易的な実装）
        for section in data.get("sections", []):
            if "グラフ" in section["content"] or "図" in section["content"]:
                tikz_code = generate_tikz_code(topic, section["content"][:200])
                if tikz_code:
                    section["figure_code"] = tikz_code
                    
        return data
    except Exception as e:
        print(f"Error writing textbook: {e}")
        return None

if __name__ == "__main__":
    # テスト実行
    result = write_textbook_chapter("2次関数")
    print(yaml.dump(result, allow_unicode=True))
