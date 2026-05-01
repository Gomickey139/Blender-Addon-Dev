FROM mcr.microsoft.com/devcontainers/python:3.10

# GUI関連の依存パッケージをすべて削除し、最低限のツールのみに
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ※Blender本体のダウンロード・解凍処理も不要になりました！