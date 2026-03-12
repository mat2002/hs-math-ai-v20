import sys
import os
import json
import time
from tqdm import tqdm

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.problem_generator import generate_problem
from ai.validator import verify_expression

def save_problem_to_db(problem_data, db_path="data/problems.json"):
    """
    生成された問題をJSONファイルに保存する。
    """
    if not os.path.exists("data"):
        os.makedirs("data")
        
    problems = []
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            try:
                problems = json.load(f)
            except:
                problems = []
                
    problems.append(problem_data)
    
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)

def main():
    curriculum = [
        {"unit": "数学I", "topics": ["数と式", "2次関数", "図形と計量", "データの分析"]},
        {"unit": "数学A", "topics": ["場合の数と確率", "図形の性質", "整数の性質"]}
    ]

    print("Starting problem generation engine...")
    
    for unit in curriculum:
        print(f"\nBuilding unit: {unit['unit']}")
        for topic in unit["topics"]:
            print(f"  Generating problems for: {topic}")
            
            # 実際にはここでループを回して大量生成するが、
            # テストとして各トピック1問ずつ生成
            try:
                p = generate_problem(topic, difficulty=3)
                if p:
                    # 数式検証（簡易版）
                    is_valid, msg = verify_expression(p.get("problem", ""))
                    if is_valid:
                        save_problem_to_db(p)
                        print(f"    [SUCCESS] Problem generated and saved.")
                    else:
                        print(f"    [FAILED] Validation error: {msg}")
                else:
                    print(f"    [FAILED] Generation error.")
            except Exception as e:
                print(f"    [ERROR] {e}")
            
            # APIのレート制限を考慮して少し待機
            time.sleep(1)

if __name__ == "__main__":
    main()
