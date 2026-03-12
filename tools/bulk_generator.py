import os
import sys
import time
import random
import concurrent.futures
from tqdm import tqdm

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.problem_generator import generate_problem
from database.schema import save_problem, init_db
from database.curriculum import get_all_topics

def worker(topic_info, difficulty, exam_type):
    """
    単一の問題を生成して保存するワーカー関数。
    """
    try:
        topic_str = f"{topic_info['unit']} - {topic_info['topic']} - {topic_info['subtopic']}"
        problem_data = generate_problem(topic_str, difficulty=difficulty, exam_type=exam_type)
        
        if problem_data:
            save_problem(topic_info['unit'], topic_info['topic'], difficulty, problem_data)
            return True
    except Exception as e:
        print(f"Worker error: {e}")
    return False

def run_bulk_generation(total_count=100, max_workers=5):
    """
    並列処理による大規模問題生成を実行する。
    """
    init_db()
    all_topics = get_all_topics()
    
    print(f"Starting bulk generation: {total_count} problems with {max_workers} workers.")
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for _ in range(total_count):
            topic_info = random.choice(all_topics)
            difficulty = random.randint(1, 5)
            exam_type = random.choice(["standard", "common_test", "hard"])
            
            futures.append(executor.submit(worker, topic_info, difficulty, exam_type))
            
        for future in tqdm(concurrent.futures.as_completed(futures), total=total_count):
            results.append(future.result())
            # APIレート制限を考慮して少し待機
            time.sleep(0.1)
            
    success_count = sum(results)
    print(f"Bulk generation completed: {success_count}/{total_count} succeeded.")

if __name__ == "__main__":
    # テストとして10問生成
    run_bulk_generation(total_count=10, max_workers=3)
