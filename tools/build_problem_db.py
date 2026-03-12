import sys
import os
import time
from tqdm import tqdm

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.problem_generator import generate_problem
from database.schema import init_db, save_problem

def main():
    # データベースの初期化
    init_db()
    
    curriculum = [
        {"unit": "数学I", "topics": ["数と式", "2次関数", "図形と計量", "データの分析"]},
        {"unit": "数学A", "topics": ["場合の数と確率", "図形の性質", "整数の性質"]}
    ]

    print("Starting large-scale problem generation engine...")
    
    # 目標生成数（テスト用に各トピック10問ずつに設定）
    # 実際にはここを数千〜数万に設定してバッチ実行する
    TARGET_PER_TOPIC = 10
    
    for unit in curriculum:
        print(f"\nBuilding unit: {unit['unit']}")
        for topic in unit["topics"]:
            print(f"  Generating {TARGET_PER_TOPIC} problems for: {topic}")
            
            # 進捗バーの表示
            for i in tqdm(range(TARGET_PER_TOPIC), desc=f"Topic: {topic}"):
                try:
                    # 難易度をランダムまたは順次設定
                    difficulty = (i % 5) + 1
                    
                    # 問題生成
                    p = generate_problem(topic, difficulty=difficulty)
                    
                    if p:
                        # データベースに保存
                        save_problem(unit['unit'], topic, difficulty, p)
                    else:
                        print(f"    [FAILED] Generation error at index {i}.")
                except Exception as e:
                    print(f"    [ERROR] {e}")
                
                # APIのレート制限を考慮して待機
                time.sleep(0.5)

if __name__ == "__main__":
    main()
