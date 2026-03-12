import os
import yaml
from openai import OpenAI
from ai.tikz_generator import generate_tikz_code
from ai.model_config import get_model_config

client = OpenAI()

def write_textbook_chapter(topic):
    """
    指定された単元について、教科書の1章分（複数の節）を執筆する。
    高度なモデルと構造化プロンプトを使用。
    """
    model_name, params = get_model_config("textbook_write")
    
    prompt = f"""
高校数学の教科書を執筆してください。

単元: {topic}

【執筆のガイドライン】
1. 導入と定義: 学習の動機付けを行い、厳密な定義を提示してください。
2. 定理と性質: 定理の主張を明確にし、必要に応じて証明や直感的な説明を加えてください。
3. 例題と解法: 基本的な例題から始め、解法のポイントを丁寧に解説してください。

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
            model=model_name,
            messages=[
                {"role": "system", "content": "あなたは高校数学の教科書執筆の専門家です。正確で論理的な解説を提供します。"},
                {"role": "user", "content": prompt}
            ],
            **params
        )
        
        content = response.choices[0].message.content
        if "---" in content:
            yaml_content = content.split("---")[1]
        else:
            yaml_content = content.replace("```yaml", "").replace("```", "")
            
        data = yaml.safe_load(yaml_content)
        
        # 各節に対して図が必要か判断し、生成する
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
