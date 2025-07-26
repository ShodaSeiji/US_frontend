#!/bin/bash

# requirements.txt に従って依存パッケージをインストール
pip install --no-cache-dir -r requirements.txt

# Streamlit を起動（ポート80で、全IPからアクセスを許可）
exec streamlit run app_streamlit.py --server.port=80 --server.address=0.0.0.0
