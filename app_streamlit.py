import streamlit as st
import pandas as pd
import requests

# ページ設定
st.set_page_config(page_title="研Q - 海外研究者マッチング", layout="wide")

# ロゴの表示（必要であればパスを修正）
st.image("logo_kenQ.png", width=250)

st.title("海外研究者マッチング - Harvard Edition")

# Step 1: 国の選択（現時点ではUSのみ）
country = st.selectbox("Select Country / 国を選んでください", ["United States"])

# Step 2: 所属（大学名）の選択
universities = [
    "Harvard University",
    "Harvard Medical School",
    "Harvard Kennedy School",
    "Harvard T.H. Chan School of Public Health"
]
university = st.selectbox("Select Institution / 所属を選んでください", universities)

# Step 3: 検索キーワードの入力
query = st.text_input("Research Topic / 研究トピックを入力", "")

# Step 4: バックエンド送信処理
if st.button("Search"):
    st.write(f"🔍 Searching papers from {university} related to '{query}'...")

    # バックエンドAPIエンドポイント（Node.js 側）
    api_url = "https://app-kenq-4.azurewebsites.net/api/search"  # 必要に応じて変更

    # 送信データ
    payload = {
        "country": country,
        "university": university,
        "query": query
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        results = response.json()

        # 結果表示
        if results:
            st.success("検索結果が見つかりました。")
            for item in results:
                st.markdown(f"### {item.get('title', 'No Title')}")
                st.markdown(f"{item.get('abstract', 'No abstract available')}")
                st.markdown("---")
        else:
            st.warning("該当する研究は見つかりませんでした。")
    except requests.exceptions.RequestException as e:
        st.error(f"APIリクエストに失敗しました: {e}")
