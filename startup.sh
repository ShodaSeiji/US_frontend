#!/bin/bash

# Azure が提供する環境変数 PORT を使用（なければ8000にフォールバック）
PORT=${PORT:-8000}

echo "Starting Streamlit application on port $PORT"
echo "Current directory: $(pwd)"

# ファイル構造の確認（デバッグ用）
echo "Directory structure:"
ls -la
echo "Pages directory:"
ls -la pages/ 2>/dev/null || echo "pages directory not found"

# 必要なパッケージのインストール
echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# main_app.pyの存在確認
if [ ! -f "main_app.py" ]; then
    echo "ERROR: main_app.py not found"
    exit 1
fi

echo "Starting Streamlit with main_app.py"

# マルチページ Streamlit アプリ起動
exec streamlit run main_app.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=false --server.headless=true