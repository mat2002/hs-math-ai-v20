import sys
import os

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.problem_generator import generate_problem

def main():
    curriculum = [
        {"unit": "数学I", "topics": ["数と式", "2次関数", "図形と計量", "データの分析"]},
        {"unit": "数学A", "topics": ["場合の数と確率", "図形の性質", "整数の性質"]}
    ]

    for unit in curriculum:
        print(f"Building unit: {unit['unit']}")
        for topic in unit["topics"]:
            print(f"  Generating problems for: {topic}")
            # 実際にはここでループを回して大量生成する
            p = generate_problem(topic)
            print(f"    Result: {p}")

if __name__ == "__main__":
    main()
