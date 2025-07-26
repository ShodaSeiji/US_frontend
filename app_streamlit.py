import streamlit as st
import pandas as pd
import requests

# ページ設定
st.set_page_config(page_title="研Q - 海外研究者マッチング", layout="wide")

# ロゴの表示
st.image("logo_kenQ.png", width=250)
st.title("海外研究者マッチング - Harvard Edition")

# Step 1: 国の選択（現在はUnited States固定）
country = st.selectbox("Select Country / 国を選んでください", ["United States"])

# Step 2: 所属大学の選択
universities = [
    "Harvard University",
    "Harvard Medical School",
    "Harvard Kennedy School",
    "Harvard T.H. Chan School of Public Health"
]
university = st.selectbox("Select Institution / 所属を選んでください", universities)

# Step 3: 研究トピックの入力
query = st.text_input("Research Topic / 研究トピックを入力", "")

# Step 4: 検索処理
if st.button("Search"):
    if not query.strip():
        st.warning("研究トピックを入力してください。")
    else:
        st.write(f"🔍 Searching researchers from **{university}** related to '**{query}**'...")

        api_url = "http://localhost:3000/api/search"  # バックエンドAPIのURL
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
                st.success("🔎 検索結果が見つかりました。")
                for item in results[:20]:
                    st.markdown(f"### 👨‍🔬 {item.get('name', 'No Name')}")
                    st.markdown(f"**Institution / 所属:** {item.get('institution', 'N/A')}")
                    st.markdown(f"**関連論文数:** {item.get('paper_count', 1)} 件")

                    with st.expander("💡 おすすめする理由を見る"):
                        st.markdown(item.get("reason", "理由は見つかりませんでした。"))

                    st.markdown("---")
            else:
                st.warning("該当する研究者は見つかりませんでした。")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ APIリクエストに失敗しました: {e}")
