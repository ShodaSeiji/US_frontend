#!/bin/bash

# Azure が提供する環境変数 PORT を使用（なければ8000にフォールバック）
PORT=${PORT:-8000}

# 必要なパッケージのインストール
pip install --no-cache-dir -r requirements.txt

# マルチページ Streamlit アプリ起動
exec streamlit run main_app.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=false