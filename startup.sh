#!/bin/bash

# Azure が提供する環境変数 PORT を使用（なければ8000にフォールバック）
PORT=${PORT:-8000}

echo "🚀 Starting Streamlit app on port $PORT"
echo "📁 Current directory: $(pwd)"
echo "📋 Files in directory:"
ls -la

# Python環境の確認
echo "🐍 Python version:"
python --version
echo "📦 Pip version:"
pip --version

# 必要なパッケージのインストール
echo "📦 Installing requirements..."
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# インストール確認
echo "✅ Checking Streamlit installation:"
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"

# Streamlit 設定ディレクトリを作成
mkdir -p ~/.streamlit

# Streamlit設定ファイルを作成
echo "⚙️ Creating Streamlit config..."
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

echo "🌐 Starting Streamlit app on 0.0.0.0:$PORT"

# メインファイルの存在確認
if [ -f "app_streamlit_v4.py" ]; then
    echo "✅ Found app_streamlit_v4.py"
    exec python -m streamlit run app_streamlit_v4.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false
elif [ -f "app_streamlit.py" ]; then
    echo "✅ Found app_streamlit.py"
    exec python -m streamlit run app_streamlit.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false
else
    echo "❌ No Streamlit app file found!"
    echo "📋 Available Python files:"
    ls -la *.py
    exit 1
fi