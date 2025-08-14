#!/bin/bash

# Azure が提供する環境変数 PORT を使用（なければ8000にフォールバック）
PORT=${PORT:-8000}

echo "🚀 Starting Streamlit app on port $PORT"
echo "📁 Current directory: $(pwd)"
echo "📋 Files in directory:"
ls -la

# 必要なパッケージのインストール
echo "📦 Installing requirements..."
pip install --no-cache-dir -r requirements.txt

# Streamlit 設定ディレクトリを作成
mkdir -p ~/.streamlit

# Streamlit設定ファイルを作成
cat > ~/.streamlit/config.toml << EOF
[server]
headless = true
port = $PORT
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
EOF

echo "⚙️ Streamlit config created"
echo "🌐 Starting app on 0.0.0.0:$PORT"

# Streamlit アプリ起動（最新版ファイル名に修正）
exec python -m streamlit run app_streamlit_v4.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false