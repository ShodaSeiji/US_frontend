import streamlit as st

# ページ設定
st.set_page_config(
    page_title="研Q - 海外研究者マッチング",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタム CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}

.feature-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1rem 0;
    transition: transform 0.2s;
}

.feature-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.status-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    text-align: center;
}

.version-info {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #007acc;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# サイドバーナビゲーション
with st.sidebar:
    st.markdown("# 🎓 研Q")
    st.markdown("### ナビゲーション")
    
    # 各ページへのリンクボタン
    st.markdown("**主要機能にアクセス:**")
    
    # 研究者検索ページへのリンク
    if st.button("🔍 Researcher Search", use_container_width=True, help="キーワードベースの高精度研究者検索"):
        st.switch_page("pages/1_Researcher_Search.py")
    
    # チャットエージェントページへのリンク  
    if st.button("🤖 Chat Agent", use_container_width=True, help="AI対話型研究者マッチング"):
        st.switch_page("pages/2_Chat_Agent.py")
    
    st.markdown("---")
    
    st.markdown("## 🎓 研Q について")
    st.markdown("海外研究者マッチングプラットフォーム")
    st.markdown("- **対象**: Harvard University関連研究者")
    st.markdown("- **データソース**: 論文データベース + 研究者情報")
    st.markdown("- **AI技術**: Azure OpenAI + Azure AI Search")
    
    st.markdown("## 🌟 主要機能")
    st.markdown("✅ **高精度ベクトル検索**")
    st.markdown("✅ **AI推薦理由生成**")
    st.markdown("✅ **多言語対応**")
    st.markdown("✅ **CSVエクスポート**")
    st.markdown("✅ **対話型エージェント**")
    st.markdown("✅ **リアルタイム検索**")
    
    st.markdown("## 📊 検索対象データ")
    st.markdown("- **研究者数**: 数千名以上")
    st.markdown("- **論文データ**: 最新の研究成果")
    st.markdown("- **所属機関**: Harvard関連組織")
    st.markdown("- **更新頻度**: 定期的に更新")
    
    st.markdown("## 🔗 サポート")
    st.markdown("技術的な質問やフィードバックは")
    st.markdown("システム管理者までお問い合わせください。")

# ロゴ表示
st.markdown("### 🎓 研Q")

# メインヘッダー
st.markdown("""
<div class="main-header">
    <h1>🎓 研Q - 海外研究者マッチングプラットフォーム</h1>
    <p>Harvard Edition - 企業の研究ニーズに最適な海外研究者を見つける</p>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🌟 利用可能な機能")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 研究者検索</h3>
        <p>キーワードベースの高精度検索で、Harvard大学関連の研究者を効率的に発見できます。</p>
        <ul>
            <li>ベクトル検索による意味的マッチング</li>
            <li>詳細フィルタリング機能</li>
            <li>研究実績メトリクス表示</li>
            <li>おすすめ理由の自動生成</li>
            <li>CSVエクスポート機能</li>
            <li>多言語対応（日本語・英語）</li>
        </ul>
        <p><strong>👈 左サイドバーから「🔍 Researcher Search」を選択してください</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🤖 対話型エージェント</h3>
        <p>AIエージェントとの対話を通じて、最適な研究者を発見できる新機能です。</p>
        <ul>
            <li>自然言語での要求定義</li>
            <li>コンテキスト理解による提案</li>
            <li>段階的な情報収集</li>
            <li>パーソナライズされた推薦</li>
            <li>リアルタイム対話</li>
            <li>多言語対応（日本語・英語）</li>
        </ul>
        <p><strong>👈 左サイドバーから「🤖 Chat Agent」を選択してください</strong></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# システム情報（本番環境用）
st.markdown("## 📊 システム情報")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="status-card">
        <h4>🚀 システム状態</h4>
        <p>運用中</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="status-card">
        <h4>🔍 検索エンジン</h4>
        <p>Azure AI Search</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="status-card">
        <h4>🤖 AI エンジン</h4>
        <p>Azure OpenAI</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="status-card">
        <h4>🌍 言語対応</h4>
        <p>日本語・English</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# バージョン情報
st.markdown("""
<div class="version-info">
    <h4>📋 最新バージョン情報</h4>
    <ul>
        <li><strong>Version 4.4.0</strong> - 多言語対応 & CSVダウンロード機能</li>
        <li><strong>新機能:</strong> 日本語・英語の切り替え対応</li>
        <li><strong>改善:</strong> 研究者数選択機能（1-10名）</li>
        <li><strong>改善:</strong> 詳細な推薦理由表示（400ワード程度）</li>
        <li><strong>新機能:</strong> 動的プレースホルダー対応</li>
        <li><strong>新機能:</strong> 完全なCSVエクスポート機能</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🎯 利用手順")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🔍 研究者を検索する**
    1. 左サイドバーから「Researcher Search」を選択
    2. 研究トピックまたはキーワードを入力
    3. 必要に応じてフィルターを設定
    4. 検索実行して結果を確認
    5. CSVでデータをダウンロード
    """)

with col2:
    st.markdown("""
    **🤖 AIエージェントと対話する**
    1. 左サイドバーから「Chat Agent」を選択
    2. 自然言語で研究ニーズを入力
    3. AIとの対話で要件を明確化
    4. 最適な研究者の提案を受け取る
    5. 詳細な推薦理由を確認
    """)

with col3:
    st.markdown("""
    **⚙️ 機能をカスタマイズする**
    1. 言語を選択（日本語・English）
    2. 表示する研究者数を調整
    3. 詳細フィルターを活用
    4. 結果をCSVでエクスポート
    5. 推薦理由の詳細を確認
    """)

st.markdown("---")

# フッター
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>© 2025 研Q (KenQ) - Harvard Researcher Matching Platform</p>
    <p>Powered by Azure AI Services | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)