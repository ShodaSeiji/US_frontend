import streamlit as st
import pandas as pd
import requests

# ページ設定
st.set_page_config(page_title="研Q - 海外研究者マッチング", layout="wide")

# ✅ カスタムCSSでResearch Metricsのデザイン改善
st.markdown("""
<style>
/* Research Metricsのフォントサイズとスタイルを統一 */
.metric-container {
    background-color: #f8f9fa;
    padding: 8px 12px;
    border-radius: 6px;
    border-left: 3px solid #0066cc;
    margin: 4px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.metric-title {
    font-size: 11px !important;
    font-weight: 600;
    color: #6c757d;
    margin-bottom: 2px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.metric-value {
    font-size: 14px !important;
    font-weight: 700;
    color: #212529;
    margin: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.metric-sub {
    font-size: 9px !important;
    color: #868e96;
    margin-top: 2px;
    font-style: italic;
}

/* 研究者名のフォントサイズ調整 - メインコンテンツとして強調 */
.researcher-name {
    font-size: 22px !important;
    font-weight: 700;
    color: #212529;
    margin-bottom: 8px;
    line-height: 1.2;
}

.researcher-info {
    font-size: 13px !important;
    color: #495057;
    margin-bottom: 4px;
    line-height: 1.4;
}

/* Research Metricsヘッダーのスタイル */
.metrics-header {
    font-size: 12px !important;
    font-weight: 600;
    color: #495057;
    margin-bottom: 8px;
    border-bottom: 1px solid #dee2e6;
    padding-bottom: 4px;
}

/* 検索結果カード全体のスタイリング */
.search-result-card {
    border: 1px solid #e9ecef;
    border-radius: 10px;
    padding: 18px;
    margin: 12px 0;
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}

/* フィルター部分のスタイリング */
.filter-section {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #dee2e6;
    margin-bottom: 20px;
}

/* 統計情報のスタイリング */
.stats-container {
    background-color: #fff;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
}

/* レスポンシブデザイン対応 */
@media (max-width: 768px) {
    .researcher-name {
        font-size: 18px !important;
    }
    .metric-value {
        font-size: 12px !important;
    }
    .metric-title {
        font-size: 10px !important;
    }
}
</style>
""", unsafe_allow_html=True)

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

# ✅ Step 4: 詳細フィルター（スタイル改善）
with st.expander("🔍 詳細フィルター（オプション）"):
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

# Step 5: 表示件数の選択
display_limit = st.selectbox("表示件数", [5, 10, 20, 50], index=1)

# Step 6: 検索処理
if st.button("Search", type="primary"):
    if not query.strip():
        st.warning("研究トピックを入力してください。")
    else:
        st.write(f"🔍 Searching researchers from **{university}** related to '**{query}**'...")

        # ✅ バックエンドAPIのURL
        api_url = "https://app-kenq-4-hweychffaqhaf8a3.canadacentral-01.azurewebsites.net/api/search"
        payload = {
            "country": country,
            "university": selected_university,
            "query": query
        }

        try:
            with st.spinner('検索中...'):
                response = requests.post(api_url, json=payload, timeout=60)  # タイムアウトを60秒に延長
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
                    
                    # ✅ 統計情報の表示（スタイル改善）
                    if len(results) > 1:
                        avg_works = sum(item.get('works_count', 0) for item in results) / len(results)
                        avg_citations = sum(item.get('cited_by_count', 0) for item in results) / len(results)
                        avg_h_index = sum(item.get('h_index', 0) for item in results) / len(results)
                        
                        with st.expander("📊 検索結果統計"):
                            st.markdown('<div class="stats-container">', unsafe_allow_html=True)
                            col1, col2, col3 = st.columns(3)
                            col1.metric("平均論文数", f"{avg_works:.0f}件")
                            col2.metric("平均被引用数", f"{avg_citations:.0f}回")
                            col3.metric("平均h指数", f"{avg_h_index:.1f}")
                            st.markdown('</div>', unsafe_allow_html=True)

                    # ✅ 研究者情報の表示（大幅デザイン改善）
                    for i, item in enumerate(display_results, 1):
                        # カード全体をHTML+CSSでスタイリング
                        st.markdown('<div class="search-result-card">', unsafe_allow_html=True)
                        
                        # 研究者基本情報
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            # ✅ 研究者名をメインコンテンツとして大きく表示
                            st.markdown(f'<h3 class="researcher-name">👨‍🔬 {item.get("name", "No Name")}</h3>', unsafe_allow_html=True)
                            
                            # ✅ 所属・分野情報を適切なサイズで表示
                            st.markdown(f'<p class="researcher-info"><strong>Institution:</strong> {item.get("institution", "N/A")}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p class="researcher-info"><strong>Research Field:</strong> {item.get("classified_field", "N/A")}</p>', unsafe_allow_html=True)

                            orcid_url = item.get("orcid", "").strip()
                            if orcid_url and orcid_url != "N/A":
                                if not orcid_url.startswith("http"):
                                    orcid_url = f"https://orcid.org/{orcid_url}"
                                st.markdown(f'<p class="researcher-info"><strong>ORCID:</strong> <a href="{orcid_url}" target="_blank">{orcid_url}</a></p>', unsafe_allow_html=True)
                            else:
                                st.markdown('<p class="researcher-info"><strong>ORCID:</strong> N/A</p>', unsafe_allow_html=True)
                        
                        with col2:
                            # ✅ Research Metricsをサブ情報として小さく整理して表示
                            st.markdown('<div style="margin-top: 10px;">', unsafe_allow_html=True)
                            st.markdown('<p class="metrics-header">📈 Research Metrics</p>', unsafe_allow_html=True)
                            
                            works_count = item.get('works_count', item.get('paper_count', 0))
                            
                            # カスタムメトリック表示
                            st.markdown(f'''
                            <div class="metric-container">
                                <div class="metric-title">論文数</div>
                                <div class="metric-value">{works_count:,}件</div>
                            </div>
                            <div class="metric-container">
                                <div class="metric-title">被引用数</div>
                                <div class="metric-value">{item.get("cited_by_count", 0):,}回</div>
                            </div>
                            <div class="metric-container">
                                <div class="metric-title">h指数</div>
                                <div class="metric-value">{item.get("h_index", 0)}</div>
                                {f'<div class="metric-sub">DB収録: {item.get("paper_data_count", 0)}件</div>' if item.get("paper_data_count") else ""}
                            </div>
                            ''', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)

                        # ✅ おすすめ理由の表示
                        with st.expander("💡 おすすめする理由を見る", expanded=False):
                            reasons_displayed = False
                            for j in range(1, 4):
                                title = item.get(f"reason_title_{j}", "").strip()
                                body = item.get(f"reason_body_{j}", "").strip()
                                if title or body:
                                    if title:
                                        st.markdown(f"**🎯 {title}**")
                                    if body:
                                        st.write(body)
                                    if j < 3 and (item.get(f"reason_title_{j+1}", "").strip() or item.get(f"reason_body_{j+1}", "").strip()):
                                        st.markdown("---")
                                    reasons_displayed = True
                            if not reasons_displayed:
                                st.write("理由は見つかりませんでした。")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown("---")
                
                else:
                    st.warning("フィルター条件に一致する研究者は見つかりませんでした。条件を緩めて再検索してください。")
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
    
    # パフォーマンス改善の案内
    st.markdown("## ⚡ パフォーマンス改善")
    st.markdown("- 多層キャッシュシステム導入")
    st.markdown("- バッチ処理で高速化")
    st.markdown("- タイムアウト時間最適化")
    st.markdown("- AI理由生成の簡潔化")