# ベースイメージとして Python 3.11 を使用
FROM python:3.11-slim

# 必要なシステムパッケージのインストール
# LaTeX (TeX Live) と TikZ に必要なパッケージを追加
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-lang-japanese \
    texlive-pictures \
    ghostscript \
    perl \
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

# データベース・出力ディレクトリの作成
RUN mkdir -p database output data

# ポートの公開
EXPOSE 5000

# Gunicorn を使用して Flask アプリを起動
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--chdir", "web", "app:app"]
