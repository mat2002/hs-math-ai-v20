import os

# AIモデルの設定
# タスクの複雑さに応じてモデルを使い分ける
MODELS = {
    "problem_gen": "gpt-4o-mini",  # 高速・安価で定型的な問題生成に最適
    "textbook_write": "gpt-4o",    # 高度な論理構成と執筆が必要な教科書作成に最適
    "tikz_gen": "gpt-4o-mini",     # TikZコードの生成
    "validator": "gpt-4o-mini"     # 数式検証
}

# パラメータ設定
PARAMS = {
    "problem_gen": {"temperature": 0.7, "max_tokens": 1000},
    "textbook_write": {"temperature": 0.5, "max_tokens": 3000},
    "tikz_gen": {"temperature": 0.3, "max_tokens": 1000},
    "validator": {"temperature": 0.0, "max_tokens": 500}  # 検証は決定論的に
}

def get_model_config(task_name):
    """
    タスク名に応じたモデル名とパラメータを返す。
    """
    return MODELS.get(task_name, "gpt-4o-mini"), PARAMS.get(task_name, {"temperature": 0.7})
