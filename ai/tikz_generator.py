import os
from ai.client import client

def generate_tikz_code(topic, problem_text):
    """
    問題の内容に合わせてTikZ図のコードを生成する。
    """
    prompt = f"""
高校数学の教材に使用するTikZ図のコードを作成してください。

単元: {topic}
問題文: {problem_text}

出力形式は、\\begin{{tikzpicture}} から \\end{{tikzpicture}} までの純粋なLaTeXコードのみとしてください。
余計な解説文やマークダウンのコードブロック（```）は含めないでください。

要件:
- 教科書風のクリーンなデザイン
- 座標軸、ラベル、重要な点などを適切に含める
- グラフの場合は、関数の形状が正確にわかるように描画する
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたはLaTeXとTikZの専門家です。正確で美しい数学図形を生成します。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        tikz_code = response.choices[0].message.content.strip()
        # 万が一マークダウンが含まれていた場合の除去
        tikz_code = tikz_code.replace("```latex", "").replace("```", "").strip()
        
        return tikz_code
    except Exception as e:
        print(f"Error generating TikZ: {e}")
        return None

if __name__ == "__main__":
    # テスト実行
    test_topic = "2次関数"
    test_problem = "$y = x^2 - 2x - 3$ のグラフを描け。"
    result = generate_tikz_code(test_topic, test_problem)
    print(result)
