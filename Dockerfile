# ベースイメージの選択
FROM python:3.10-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev

# アプリケーションの依存関係をインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . /app

# Flaskの環境変数を設定
ENV FLASK_APP=app.main
ENV FLASK_ENV=production

# ポートを開放
EXPOSE 8000

# アプリケーションを起動
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app.main:app"]