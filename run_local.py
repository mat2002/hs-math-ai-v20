import os
import sys
import subprocess

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_local():
    print("ローカル環境で高校数学教材AI v20を起動します...")
    print("Webサーバーは http://127.0.0.1:5000 で利用可能です。")
    
    # Flaskアプリケーションを起動
    # 環境変数 FLASK_APP を設定し、Flaskのrunコマンドを使用
    env = os.environ.copy()
    env["FLASK_APP"] = "web/app.py"
    env["FLASK_ENV"] = "development" # 開発モードで起動
    
    try:
        subprocess.run(
            ["flask", "run"],
            env=env, # 環境変数を渡す
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Flaskアプリケーションの起動に失敗しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_local()
