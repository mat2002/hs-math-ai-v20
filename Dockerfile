# ベースイメージとして Python 3.11 を使用
FROM python:3.11-slim

# 必要なシステムパッケージのインストール
# TeX Live 2026 が既にインストールされている環境を想定し、
# 必要な依存関係（perl, ghostscript等）のみを最小限にインストールします。
RUN apt-get update && apt-get install -y \
    perl \
    ghostscript \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /app

# 依存ライブラリのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルのコピー
COPY . .

# 出力ディレクトリの作成
RUN mkdir -p output data

# ポートの公開
EXPOSE 5000

# Gunicorn を使用して Flask アプリを起動
# 実行時に TeX Live 2026 のパスが通っていることを前提とします
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--chdir", "web", "app:app"]
