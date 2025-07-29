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

        api_url = "https://app-kenq-4-hweychffaqhaf8a3.canadacentral-01.azurewebsites.net/api/search"  # バックエンドAPIのURL
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
                display_limit = 10  # 表示件数の上限を変数化
                st.success(f"🔎検索結果（上位 {min(display_limit, len(results))} 件）を表示します。")

                for item in results[:display_limit]:
                    st.markdown(f"### 👨‍🔬 {item.get('name', 'No Name')}")
                    st.markdown(f"**Institution / 所属:** {item.get('institution', 'N/A')}")
                    # 🔁 ORCID出力に変更（リンク形式）
                    orcid_url = item.get("orcid", "").strip()
                    if orcid_url:
                        st.markdown(f"**ORCID:** [{orcid_url}]({orcid_url})")
                    else:
                        st.markdown("**ORCID:** N/A")
                    with st.expander("💡 おすすめする理由を見る"):
                        reasons_displayed = False
                        for i in range(1, 4):
                            title = item.get(f"reason_title_{i}", "").strip()
                            body = item.get(f"reason_body_{i}", "").strip()
                            if title or body:
                                if title:
                                    st.markdown(f"**{title}**")
                                if body:
                                    st.write(body)
                                st.markdown("---")
                                reasons_displayed = True
                        if not reasons_displayed:
                            st.write("理由は見つかりませんでした。")
                    st.markdown("---")
            else:
                st.warning("該当する研究者は見つかりませんでした。")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ APIリクエストに失敗しました: {e}")
