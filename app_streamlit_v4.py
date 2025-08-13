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
    "All",
    "Harvard University",
    "Harvard Medical School",
    "Harvard Kennedy School",
    "Harvard T.H. Chan School of Public Health",
    "Harvard Business School",
    "Harvard School of Engineering and Applied Sciences",
    "Harvard Divinity School",
    "Harvard Graduate School of Education",
    "Harvard Law School"
]
university = st.selectbox("Select Institution / 所属を選んでください", universities)
selected_university = "" if university == "All" else university.strip()

# Step 3: 研究トピックの入力
query = st.text_input("Research Topic / 研究トピックを入力", key="research_query")

# ✅ Step 4: 詳細フィルター（新機能）
with st.expander("🔍 詳細フィルター（オプション）"):
    col1, col2 = st.columns(2)
    
    with col1:
        min_works = st.number_input("最小論文数", min_value=0, value=0, step=10)
        min_citations = st.number_input("最小被引用数", min_value=0, value=0, step=100)
    
    with col2:
        min_h_index = st.number_input("最小h指数", min_value=0, value=0, step=5)
        research_fields = st.multiselect(
            "研究分野",
            ["Arts_Sciences", "Medical", "Engineering", "Business", "Law", "Education"],
            default=[]
        )

# Step 5: 表示件数の選択
display_limit = st.selectbox("表示件数", [5, 10, 20, 50], index=1)

# Step 6: 検索処理
if st.button("Search", type="primary"):
    if not query.strip():
        st.warning("研究トピックを入力してください。")
    else:
        st.write(f"🔍 Searching researchers from **{university}** related to '**{query}**'...")

        # ✅ バックエンドAPIのURL（本番環境に応じて変更）
        api_url = "https://app-kenq-4-hweychffaqhaf8a3.canadacentral-01.azurewebsites.net/api/search"
        # api_url = "http://localhost:3000/api/search"  # ローカルテスト用
        # api_url = "https://app-kenq-4-hweychffaqhaf8a3.canadacentral-01.azurewebsites.net/api/search" #本番用
        payload = {
            "country": country,
            "university": selected_university,
            "query": query
        }

        try:
            with st.spinner('検索中...'):
                response = requests.post(api_url, json=payload, timeout=30)
                response.raise_for_status()
                results = response.json()

            # 結果表示
            if results:
                # ✅ フィルタリング（フロントエンド側）
                filtered_results = []
                for item in results:
                    # 論文数フィルター
                    if min_works > 0 and item.get('works_count', 0) < min_works:
                        continue
                    # 被引用数フィルター
                    if min_citations > 0 and item.get('cited_by_count', 0) < min_citations:
                        continue
                    # h指数フィルター
                    if min_h_index > 0 and item.get('h_index', 0) < min_h_index:
                        continue
                    # 研究分野フィルター
                    if research_fields and item.get('classified_field', '') not in research_fields:
                        continue
                    
                    filtered_results.append(item)

                # 表示件数制限
                display_results = filtered_results[:display_limit]
                
                if display_results:
                    st.success(f"🔎検索結果（{len(display_results)}件 / 全{len(results)}件中）を表示します。")
                    
                    # ✅ 統計情報の表示
                    if len(results) > 1:
                        avg_works = sum(item.get('works_count', 0) for item in results) / len(results)
                        avg_citations = sum(item.get('cited_by_count', 0) for item in results) / len(results)
                        avg_h_index = sum(item.get('h_index', 0) for item in results) / len(results)
                        
                        with st.expander("📊 検索結果統計"):
                            col1, col2, col3 = st.columns(3)
                            col1.metric("平均論文数", f"{avg_works:.0f}件")
                            col2.metric("平均被引用数", f"{avg_citations:.0f}回")
                            col3.metric("平均h指数", f"{avg_h_index:.1f}")

                    # 研究者情報の表示
                    for i, item in enumerate(display_results, 1):
                        st.markdown("---")
                        
                        # ✅ 研究者基本情報（強化版）
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"### 👨‍🔬 {item.get('name', 'No Name')}")
                            st.markdown(f"**Institution / 所属:** {item.get('institution', 'N/A')}")
                            st.markdown(f"**Research Field / 研究分野:** {item.get('classified_field', 'N/A')}")

                            orcid_url = item.get("orcid", "").strip()
                            if orcid_url and orcid_url != "N/A":
                                if not orcid_url.startswith("http"):
                                    orcid_url = f"https://orcid.org/{orcid_url}"
                                st.markdown(f"**ORCID:** [{orcid_url}]({orcid_url})")
                            else:
                                st.markdown("**ORCID:** N/A")
                        
                        with col2:
                            # ✅ 研究実績メトリクス
                            st.markdown("**📈 Research Metrics**")
                            
                            # works_countとpaper_countの両方に対応
                            works_count = item.get('works_count', item.get('paper_count', 0))
                            st.metric("論文数", f"{works_count:,}件")
                            st.metric("被引用数", f"{item.get('cited_by_count', 0):,}回")
                            st.metric("h指数", item.get('h_index', 0))
                            
                            # CSVデータでの論文件数も表示
                            if item.get('paper_data_count'):
                                st.caption(f"データベース収録論文: {item.get('paper_data_count')}件")

                        # ✅ おすすめ理由の表示（強化版）
                        with st.expander("💡 おすすめする理由を見る", expanded=False):
                            reasons_displayed = False
                            for j in range(1, 4):
                                title = item.get(f"reason_title_{j}", "").strip()
                                body = item.get(f"reason_body_{j}", "").strip()
                                if title or body:
                                    if title:
                                        st.markdown(f"**🎯 理由{j}: {title}**")
                                    if body:
                                        st.write(body)
                                    if j < 3:  # 最後以外は区切り線
                                        st.markdown("---")
                                    reasons_displayed = True
                            if not reasons_displayed:
                                st.write("理由は見つかりませんでした。")
                
                else:
                    st.warning("フィルター条件に一致する研究者は見つかりませんでした。条件を緩めて再検索してください。")
                    
                    # フィルター前の件数を表示
                    if len(results) > 0:
                        st.info(f"フィルター適用前は{len(results)}件の結果がありました。")
                        
            else:
                st.warning("該当する研究者は見つかりませんでした。")

        except requests.exceptions.Timeout:
            st.error("⏰ 検索がタイムアウトしました。しばらく待ってから再度お試しください。")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ APIリクエストに失敗しました: {e}")
            if "localhost" in api_url:
                st.info("💡 ローカルサーバーが起動しているか確認してください。")
        except Exception as e:
            st.error(f"❌ 予期しないエラーが発生しました: {e}")

# ✅ サイドバーに情報を追加
with st.sidebar:
    st.markdown("## 📊 システム情報")
    st.markdown("- **データベース**: Harvard研究者データ")
    st.markdown("- **インデックス**: harvard-index-v6")
    st.markdown("- **検索エンジン**: Azure AI Search")
    st.markdown("- **AI**: Azure OpenAI")
    
    st.markdown("## 🔍 検索のコツ")
    st.markdown("- 英語・日本語どちらでも検索可能")
    st.markdown("- 具体的なキーワードを使用")
    st.markdown("- 詳細フィルターで絞り込み可能")
    
    st.markdown("## 📈 表示される指標")
    st.markdown("- **論文数**: 研究者の総論文数")
    st.markdown("- **被引用数**: 論文の被引用回数")
    st.markdown("- **h指数**: 研究影響力の指標")