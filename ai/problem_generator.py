from openai import OpenAI

client = OpenAI()

def generate_problem(topic):
    """
    高校数学の問題を生成する
    """
    prompt = f"""
高校数学の問題を作成してください

単元: {topic}

出力形式
YAML
problem: |
  (問題文)
solution: |
  (解答・解説)
difficulty: (1-5)
"""
    # 実際にはここでLLMを呼び出す
    # response = client.chat.completions.create(...)
    return "Generated problem for " + topic
