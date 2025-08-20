import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime

# ページ設定
st.set_page_config(page_title="研Q - 海外研究者マッチング", layout="wide")

# ✅ セッション状態で言語管理
if 'language' not in st.session_state:
    st.session_state.language = 'ja'  # デフォルトは日本語

# ✅ 検索結果をセッション状態で保存
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'last_search_query' not in st.session_state:
    st.session_state.last_search_query = ""

# ✅ 言語設定関数
def get_text(key):
    texts = {
        'ja': {
            'title': '海外研究者マッチング - Harvard Edition',
            'select_country': 'Select Country / 国を選んでください',
            'select_institution': 'Select Institution / 所属を選んでください',
            'research_topic': 'Research Topic / 研究トピックを入力',
            'detailed_filter': '🔍 詳細フィルター（オプション）',
            'min_papers': 'Number of publications / 最小論文数',
            'min_citations': 'Number of citations / 最小被引用数',
            'min_h_index': 'h-index / 最小h指数',
            'research_fields': '研究分野',
            'num_results': 'Number of results / 表示件数',
            'search_button': 'Search',
            'enter_topic': '研究トピックを入力してください。',
            'searching': '検索中...',
            'search_results': '🔎検索結果（{count}件 / 全{total}件中）を表示します。',
            'search_stats': '📊 検索結果統計',
            'avg_papers': '平均論文数',
            'avg_citations': '平均被引用数',
            'avg_h_index': '平均h指数',
            'papers_unit': '件',
            'citations_unit': '回',
            'researcher_name': '👨‍🔬 {name}',
            'institution': 'Institution',
            'research_field': 'Research Field',
            'orcid': 'ORCID',
            'research_metrics': '📈 Research Metrics',
            'num_publications': 'Number of publications / 論文数',
            'num_citations': 'Number of citations / 被引用数',
            'h_index': 'h-index / h指数',
            'db_records': 'DBデータ',
            'view_reasons': '💡 おすすめする理由を見る',
            'no_reasons': '理由は見つかりませんでした。',
            'no_filter_results': 'フィルター条件に一致する研究者は見つかりませんでした。条件を緩めて再検索してください。',
            'filter_before': 'フィルター適用前は{count}件の結果がありました。',
            'no_results': '該当する研究者は見つかりませんでした。',
            'timeout_error': '⏰ 検索がタイムアウトしました。しばらく待ってから再度お試しください。',
            'api_error': '❌ APIリクエストに失敗しました: {error}',
            'localhost_info': '💡 ローカルサーバーが起動しているか確認してください。',
            'unexpected_error': '❌ 予期しないエラーが発生しました: {error}',
            'system_info': '## 📊 システム情報',
            'database': '**データベース**: Harvardデータ',
            'index': '**インデックス**: harvard-index-v6',
            'search_engine': '**検索エンジン**: Azure AI Search',
            'ai': '**AI**: Azure OpenAI',
            'search_tips': '## 🔍 検索のコツ',
            'search_tip1': '- 英語・日本語どちらでも検索可能',
            'search_tip2': '- 具体的なキーワードを使用',
            'search_tip3': '- 詳細フィルターで絞り込み可能',
            'metrics_info': '## 📈 表示される指標',
            'metrics_info1': '- **論文数**: 研究者の総論文数',
            'metrics_info2': '- **被引用数**: 論文の被引用回数',
            'metrics_info3': '- **h指数**: 研究影響力の指標',
            'performance': '## ⚡ パフォーマンス改善',
            'performance1': '- 多層キャッシュシステム導入',
            'performance2': '- バッチ処理で高速化',
            'performance3': '- タイムアウト時間最適化',
            'performance4': '- AI理由生成の簡潔化',
            'download_csv': '📥 CSVダウンロード',
            'download_button': 'Download CSV',
            'download_filename': 'harvard_researchers_{timestamp}.csv',
            'download_success': '✅ CSVファイルをダウンロードしました',
            'download_error': '❌ CSVダウンロードに失敗しました: {error}',
            'no_data_download': '⚠️ ダウンロードするデータがありません。まず検索を実行してください。'
        },
        'en': {
            'title': 'International Researcher Matching - Harvard Edition',
            'select_country': 'Select Country',
            'select_institution': 'Select Institution',
            'research_topic': 'Research Topic',
            'detailed_filter': '🔍 Advanced Filters (Optional)',
            'min_papers': 'Minimum publications',
            'min_citations': 'Minimum citations',
            'min_h_index': 'Minimum h-index',
            'research_fields': 'Research Fields',
            'num_results': 'Number of results',
            'search_button': 'Search',
            'enter_topic': 'Please enter a research topic.',
            'searching': 'Searching...',
            'search_results': '🔎Search Results ({count} of {total} total)',
            'search_stats': '📊 Search Statistics',
            'avg_papers': 'Avg Publications',
            'avg_citations': 'Avg Citations',
            'avg_h_index': 'Avg h-index',
            'papers_unit': 'papers',
            'citations_unit': 'times',
            'researcher_name': '👨‍🔬 {name}',
            'institution': 'Institution',
            'research_field': 'Research Field',
            'orcid': 'ORCID',
            'research_metrics': '📈 Research Metrics',
            'num_publications': 'Publications',
            'num_citations': 'Citations',
            'h_index': 'h-index',
            'db_records': 'DB Records',
            'view_reasons': '💡 Why We Recommend This Researcher',
            'no_reasons': 'No reasons found.',
            'no_filter_results': 'No researchers match the filter criteria. Please relax the conditions and search again.',
            'filter_before': 'There were {count} results before applying filters.',
            'no_results': 'No matching researchers found.',
            'timeout_error': '⏰ Search timed out. Please wait and try again.',
            'api_error': '❌ API request failed: {error}',
            'localhost_info': '💡 Please check if the local server is running.',
            'unexpected_error': '❌ An unexpected error occurred: {error}',
            'system_info': '## 📊 System Information',
            'database': '**Database**: Harvard Data',
            'index': '**Index**: harvard-index-v6',
            'search_engine': '**Search Engine**: Azure AI Search',
            'ai': '**AI**: Azure OpenAI',
            'search_tips': '## 🔍 Search Tips',
            'search_tip1': '- Search in English or Japanese',
            'search_tip2': '- Use specific keywords',
            'search_tip3': '- Use advanced filters to narrow results',
            'metrics_info': '## 📈 Displayed Metrics',
            'metrics_info1': '- **Publications**: Total number of papers',
            'metrics_info2': '- **Citations**: Citation count',
            'metrics_info3': '- **h-index**: Research impact indicator',
            'performance': '## ⚡ Performance Improvements',
            'performance1': '- Multi-layer caching system',
            'performance2': '- Batch processing optimization',
            'performance3': '- Optimized timeout settings',
            'performance4': '- Streamlined AI reasoning',
            'download_csv': '📥 CSV Download',
            'download_button': 'Download CSV',
            'download_filename': 'harvard_researchers_{timestamp}.csv',
            'download_success': '✅ CSV file downloaded successfully',
            'download_error': '❌ CSV download failed: {error}',
            'no_data_download': '⚠️ No data to download. Please run a search first.'
        }
    }
    return texts.get(st.session_state.language, texts['ja']).get(key, key)

# ✅ CSVデータ準備関数
def prepare_csv_data(results, query, language='ja'):
    """検索結果をCSV用のDataFrameに変換"""
    if not results:
        return None
    
    csv_data = []
    for item in results:
        # 基本情報
        row = {
            'Researcher Name / 研究者名': item.get('name', 'N/A'),
            'Institution / 所属': item.get('institution', 'N/A'),
            'Research Field / 研究分野': item.get('classified_field', 'N/A'),
            'ORCID': item.get('orcid', 'N/A'),
            'Publications / 論文数': item.get('works_count', 0),
            'Citations / 被引用数': item.get('cited_by_count', 0),
            'h-index / h指数': item.get('h_index', 0),
            'DB Records / DBデータ': item.get('paper_data_count', 0),
        }
        
        # おすすめ理由を追加
        for i in range(1, 4):
            title_key = f'reason_title_{i}'
            body_key = f'reason_body_{i}'
            
            if language == 'en':
                row[f'Recommendation Reason {i} Title'] = item.get(title_key, '')
                row[f'Recommendation Reason {i} Details'] = item.get(body_key, '')
            else:
                row[f'おすすめ理由{i}タイトル'] = item.get(title_key, '')
                row[f'おすすめ理由{i}詳細'] = item.get(body_key, '')
        
        csv_data.append(row)
    
    df = pd.DataFrame(csv_data)
    
    # メタデータを追加
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if language == 'en':
        metadata_row = {
            'Researcher Name / 研究者名': f'Search Query: {query}',
            'Institution / 所属': f'Generated: {timestamp}',
            'Research Field / 研究分野': f'Total Results: {len(results)}',
            'ORCID': 'Language: English',
            'Publications / 論文数': '',
            'Citations / 被引用数': '',
            'h-index / h指数': '',
            'DB Records / DBデータ': '',
        }
    else:
        metadata_row = {
            'Researcher Name / 研究者名': f'検索クエリ: {query}',
            'Institution / 所属': f'生成日時: {timestamp}',
            'Research Field / 研究分野': f'総結果数: {len(results)}件',
            'ORCID': '言語: 日本語',
            'Publications / 論文数': '',
            'Citations / 被引用数': '',
            'h-index / h指数': '',
            'DB Records / DBデータ': '',
        }
    
    # 理由の列も空で埋める
    for i in range(1, 4):
        if language == 'en':
            metadata_row[f'Recommendation Reason {i} Title'] = ''
            metadata_row[f'Recommendation Reason {i} Details'] = ''
        else:
            metadata_row[f'おすすめ理由{i}タイトル'] = ''
            metadata_row[f'おすすめ理由{i}詳細'] = ''
    
    # メタデータを先頭に挿入
    df = pd.concat([pd.DataFrame([metadata_row]), df], ignore_index=True)
    
    return df

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

/* 言語切り替えボタンのスタイル */
.language-button {
    background-color: #ffffff;
    border: 2px solid #0066cc;
    border-radius: 8px;
    padding: 8px 16px;
    margin: 2px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

.language-button.active {
    background-color: #0066cc;
    color: white;
}

.language-button:hover {
    background-color: #f0f8ff;
}

/* CSVダウンロードボタンのスタイル */
.download-section {
    background-color: #e8f5e8;
    border: 1px solid #28a745;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
    text-align: center;
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

# ✅ 言語切り替えボタン
st.markdown("### Language / 言語選択")
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🇯🇵 日本語", key="btn_ja", 
                help="日本語で表示", 
                use_container_width=True):
        st.session_state.language = 'ja'
        st.rerun()

with col2:
    if st.button("🇺🇸 English", key="btn_en", 
                help="Display in English", 
                use_container_width=True):
        st.session_state.language = 'en'
        st.rerun()

# 現在の言語を表示
current_lang_display = "🇯🇵 日本語" if st.session_state.language == 'ja' else "🇺🇸 English"
st.write(f"**Current Language / 現在の言語**: {current_lang_display}")

# ロゴの表示
st.image("logo_kenQ.png", width=250)
st.title(get_text('title'))

# Step 1: 国の選択（現在はUnited States固定）
country = st.selectbox(get_text('select_country'), ["United States"])

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
university = st.selectbox(get_text('select_institution'), universities)
selected_university = "" if university == "All" else university.strip()

# Step 3: 研究トピックの入力
query = st.text_input(get_text('research_topic'), key="research_query")

# ✅ Step 4: 詳細フィルター（多言語対応）
with st.expander(get_text('detailed_filter')):
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        min_works = st.number_input(get_text('min_papers'), min_value=0, value=0, step=10)
        min_citations = st.number_input(get_text('min_citations'), min_value=0, value=0, step=100)
    
    with col2:
        min_h_index = st.number_input(get_text('min_h_index'), min_value=0, value=0, step=5)
        research_fields = st.multiselect(
            get_text('research_fields'),
            ["Arts_Sciences", "Medical", "Engineering", "Business", "Law", "Education"],
            default=[]
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Step 5: 表示件数の選択
display_limit = st.selectbox(get_text('num_results'), [5, 10, 20, 50], index=1)

# ✅ CSVダウンロードセクション（検索結果がある場合のみ表示）
if st.session_state.search_results:
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    st.markdown(f"### {get_text('download_csv')}")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(get_text('download_button'), type="secondary", use_container_width=True):
            try:
                # CSVデータの準備
                csv_df = prepare_csv_data(
                    st.session_state.search_results, 
                    st.session_state.last_search_query,
                    st.session_state.language
                )
                
                if csv_df is not None:
                    # CSVとしてエンコード
                    csv_buffer = io.StringIO()
                    csv_df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
                    csv_data = csv_buffer.getvalue()
                    
                    # ファイル名の生成
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = get_text('download_filename').format(timestamp=timestamp)
                    
                    # ダウンロードボタン
                    st.download_button(
                        label=f"📥 {filename}",
                        data=csv_data,
                        file_name=filename,
                        mime="text/csv",
                        use_container_width=True
                    )
                    st.success(get_text('download_success'))
                else:
                    st.error(get_text('no_data_download'))
                    
            except Exception as e:
                st.error(get_text('download_error').format(error=str(e)))
    
    st.markdown('</div>', unsafe_allow_html=True)

# Step 6: 検索処理
if st.button(get_text('search_button'), type="primary"):
    if not query.strip():
        st.warning(get_text('enter_topic'))
    else:
        st.write(f"🔍 Searching researchers from **{university}** related to '**{query}**'...")

        # ✅ バックエンドAPIのURL
        api_url = "https://app-kenq-4-hweychffaqhaf8a3.canadacentral-01.azurewebsites.net/api/search"
        payload = {
            "country": country,
            "university": selected_university,
            "query": query,
            "language": st.session_state.language  # ✅ 言語パラメータ追加
        }

        try:
            with st.spinner(get_text('searching')):
                response = requests.post(api_url, json=payload, timeout=60)
                response.raise_for_status()
                results = response.json()

            # 結果表示
            if results:
                # ✅ 検索結果をセッション状態に保存
                st.session_state.search_results = results
                st.session_state.last_search_query = query
                
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
                    st.success(get_text('search_results').format(count=len(display_results), total=len(results)))
                    
                    # ✅ 統計情報の表示（多言語対応）
                    if len(results) > 1:
                        avg_works = sum(item.get('works_count', 0) for item in results) / len(results)
                        avg_citations = sum(item.get('cited_by_count', 0) for item in results) / len(results)
                        avg_h_index = sum(item.get('h_index', 0) for item in results) / len(results)
                        
                        with st.expander(get_text('search_stats')):
                            st.markdown('<div class="stats-container">', unsafe_allow_html=True)
                            col1, col2, col3 = st.columns(3)
                            col1.metric(get_text('avg_papers'), f"{avg_works:.0f}{get_text('papers_unit')}")
                            col2.metric(get_text('avg_citations'), f"{avg_citations:.0f}{get_text('citations_unit')}")
                            col3.metric(get_text('avg_h_index'), f"{avg_h_index:.1f}")
                            st.markdown('</div>', unsafe_allow_html=True)

                    # ✅ 研究者情報の表示（多言語対応）
                    for i, item in enumerate(display_results, 1):
                        # カード全体をHTML+CSSでスタイリング
                        st.markdown('<div class="search-result-card">', unsafe_allow_html=True)
                        
                        # 研究者基本情報
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            # ✅ 研究者名をメインコンテンツとして大きく表示
                            st.markdown(f'<h3 class="researcher-name">{get_text("researcher_name").format(name=item.get("name", "No Name"))}</h3>', unsafe_allow_html=True)
                            
                            # ✅ 所属・分野情報を適切なサイズで表示
                            st.markdown(f'<p class="researcher-info"><strong>{get_text("institution")}:</strong> {item.get("institution", "N/A")}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p class="researcher-info"><strong>{get_text("research_field")}:</strong> {item.get("classified_field", "N/A")}</p>', unsafe_allow_html=True)

                            orcid_url = item.get("orcid", "").strip()
                            if orcid_url and orcid_url != "N/A":
                                if not orcid_url.startswith("http"):
                                    orcid_url = f"https://orcid.org/{orcid_url}"
                                st.markdown(f'<p class="researcher-info"><strong>{get_text("orcid")}:</strong> <a href="{orcid_url}" target="_blank">{orcid_url}</a></p>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<p class="researcher-info"><strong>{get_text("orcid")}:</strong> N/A</p>', unsafe_allow_html=True)
                        
                        with col2:
                            # ✅ Research Metricsをサブ情報として小さく整理して表示
                            st.markdown('<div style="margin-top: 10px;">', unsafe_allow_html=True)
                            st.markdown(f'<p class="metrics-header">{get_text("research_metrics")}</p>', unsafe_allow_html=True)
                            
                            works_count = item.get('works_count', item.get('paper_count', 0))
                            
                            # カスタムメトリック表示
                            papers_unit = get_text('papers_unit')
                            citations_unit = get_text('citations_unit')
                            db_records = get_text('db_records')
                            
                            st.markdown(f'''
                            <div class="metric-container">
                                <div class="metric-title">{get_text('num_publications')}</div>
                                <div class="metric-value">{works_count:,}{papers_unit}</div>
                            </div>
                            <div class="metric-container">
                                <div class="metric-title">{get_text('num_citations')}</div>
                                <div class="metric-value">{item.get("cited_by_count", 0):,}{citations_unit}</div>
                            </div>
                            <div class="metric-container">
                                <div class="metric-title">{get_text('h_index')}</div>
                                <div class="metric-value">{item.get("h_index", 0)}</div>
                                {f'<div class="metric-sub">{db_records}: {item.get("paper_data_count", 0)}{papers_unit}</div>' if item.get("paper_data_count") else ""}
                            </div>
                            ''', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)

                        # ✅ おすすめ理由の表示（多言語対応）
                        with st.expander(get_text('view_reasons'), expanded=False):
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
                                st.write(get_text('no_reasons'))
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown("---")
                
                else:
                    st.warning(get_text('no_filter_results'))
                    if len(results) > 0:
                        st.info(get_text('filter_before').format(count=len(results)))
                        
            else:
                st.warning(get_text('no_results'))
                # 結果がない場合はセッション状態をクリア
                st.session_state.search_results = []

        except requests.exceptions.Timeout:
            st.error(get_text('timeout_error'))
        except requests.exceptions.RequestException as e:
            st.error(get_text('api_error').format(error=str(e)))
            if "localhost" in api_url:
                st.info(get_text('localhost_info'))
        except Exception as e:
            st.error(get_text('unexpected_error').format(error=str(e)))

# ✅ サイドバーに情報を追加（多言語対応）
with st.sidebar:
    st.markdown(get_text('system_info'))
    st.markdown(f"- {get_text('database')}")
    st.markdown(f"- {get_text('index')}")
    st.markdown(f"- {get_text('search_engine')}")
    st.markdown(f"- {get_text('ai')}")
    
    st.markdown(get_text('search_tips'))
    st.markdown(get_text('search_tip1'))
    st.markdown(get_text('search_tip2'))
    st.markdown(get_text('search_tip3'))
    
    st.markdown(get_text('metrics_info'))
    st.markdown(get_text('metrics_info1'))
    st.markdown(get_text('metrics_info2'))
    st.markdown(get_text('metrics_info3'))
    
    # パフォーマンス改善の案内
    st.markdown(get_text('performance'))
    st.markdown(get_text('performance1'))
    st.markdown(get_text('performance2'))
    st.markdown(get_text('performance3'))
    st.markdown(get_text('performance4'))
    
    # ✅ CSVダウンロード機能の説明
    if st.session_state.search_results:
        st.markdown("## 📥 CSV Export")
        if st.session_state.language == 'en':
            st.markdown("- Export search results to CSV")
            st.markdown("- Includes all researcher data")
            st.markdown("- Contains recommendation reasons")
            st.markdown("- Multi-language support")
        else:
            st.markdown("- 検索結果をCSVでエクスポート")
            st.markdown("- 全研究者データを含む")
            st.markdown("- おすすめ理由も含まれます")
            st.markdown("- 多言語対応")