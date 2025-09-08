import streamlit as st
import requests
import json
from datetime import datetime
import re
import pandas as pd
import io

# ページ設定
st.set_page_config(page_title="研Q - 対話型エージェント", layout="wide")

# 🔧 改修機能1: 言語設定の初期化
if 'language' not in st.session_state:
    st.session_state.language = "日本語"

# 🔧 改修機能1: 言語選択機能
col_lang1, col_lang2, col_lang3 = st.columns([1, 1, 3])
with col_lang1:
    st.markdown("**Language / 言語選択**")
with col_lang2:
    language_option = st.selectbox(
        "",
        options=["日本語", "English"],
        index=0 if st.session_state.language == "日本語" else 1,
        key="language_selector"
    )
    st.session_state.language = language_option

# 言語に基づくテキスト定義
def get_text(key):
    texts = {
        "日本語": {
            "title": "🤖 研Q対話型エージェント",
            "description": "**企業の研究ニーズに最適な海外研究者を見つけるAIエージェントです。**  \nチャット形式で質問にお答えしながら、候補研究者をご提案いたします。",
            "chat_history": "💬 会話履歴",
            "recommended_researchers": "🎯 おすすめ研究者",
            "input_placeholder": "メッセージを入力してください:",
            "send_button": "送信",
            "test_connection": "接続テスト",
            "connection_success": "✅ APIサーバーとの接続に成功しました！",
            "connection_failed": "❌ 接続テストに失敗しました:",
            "researcher_count": "表示する研究者数:",
            "current_setting": "現在の設定:",
            "researchers_display": "名の研究者を表示",
            "csv_download": "📥 CSVダウンロード",
            "download_csv": "Download CSV",
            "system_info": "🔧 システム情報",
            "display_settings": "⚙️ 表示設定",
            "context_info": "📋 現在の会話コンテキスト",
            "reset_chat": "🔄 会話をリセット",
            "placeholder_function": "💡 プレースホルダー機能",
            "usage_tips": "💡 使い方のヒント",
            "debug_info": "🐛 デバッグ情報",
            "institution": "所属:",
            "research_field": "研究分野:",
            "orcid": "ORCID:",
            "papers": "論文数",
            "citations": "被引用数",
            "h_index": "h指数",
            "reason_title": "🎯 おすすめする理由",
            "reason_generating": "おすすめ理由は現在生成中です。しばらくお待ちください。"
        },
        "English": {
            "title": "🤖 KenQ Chat Agent",
            "description": "**AI agent to find the best overseas researchers for your corporate research needs.**  \nWe will suggest candidate researchers while answering your questions in a chat format.",
            "chat_history": "💬 Chat History",
            "recommended_researchers": "🎯 Recommended Researchers",
            "input_placeholder": "Enter your message:",
            "send_button": "Send",
            "test_connection": "Test Connection",
            "connection_success": "✅ Successfully connected to API server!",
            "connection_failed": "❌ Connection test failed:",
            "researcher_count": "Number of researchers to display:",
            "current_setting": "Current setting:",
            "researchers_display": " researchers to display",
            "csv_download": "📥 CSV Download",
            "download_csv": "Download CSV",
            "system_info": "🔧 System Information",
            "display_settings": "⚙️ Display Settings",
            "context_info": "📋 Current Context",
            "reset_chat": "🔄 Reset Chat",
            "placeholder_function": "💡 Placeholder Function",
            "usage_tips": "💡 Usage Tips",
            "debug_info": "🐛 Debug Information",
            "institution": "Institution:",
            "research_field": "Research Field:",
            "orcid": "ORCID:",
            "papers": "Papers",
            "citations": "Citations",
            "h_index": "h-index",
            "reason_title": "🎯 Reasons for Recommendation",
            "reason_generating": "Recommendation reasons are currently being generated. Please wait."
        }
    }
    return texts[st.session_state.language].get(key, key)

# ロゴの表示
st.markdown("### 🎓 研Q")
st.title(get_text("title"))
st.markdown(get_text("description"))

# API設定
API_BASE_URL = "https://app-kenq-4-hweychffaqhaf8a3.canadacentral-01.azurewebsites.net"
# 本番環境用: API_BASE_URL = "https://app-kenq-4-hweychffaqhaf8a3.canadacentral-01.azurewebsites.net"
# テスト環境用："http://localhost:3000"


# 🔧 改修機能2: CSVダウンロード機能
def create_csv_from_researchers(researchers):
    """研究者データからCSVを生成"""
    if not researchers:
        return None
    
    # CSVデータ用のリストを作成
    csv_data = []
    
    for i, researcher in enumerate(researchers, 1):
        csv_data.append({
            "No.": i,
            "Name / 研究者名": researcher.get('name', 'N/A'),
            "Institution / 所属": researcher.get('institution', 'N/A'),
            "Research Field / 研究分野": researcher.get('classified_field', 'N/A'),
            "Papers / 論文数": researcher.get('works_count', 0),
            "Citations / 被引用数": researcher.get('cited_by_count', 0),
            "h-index / h指数": researcher.get('h_index', 0),
            "ORCID": researcher.get('orcid', 'N/A'),
            "Reason 1 Title / 理由1 タイトル": researcher.get('reason_title_1', ''),
            "Reason 1 Body / 理由1 詳細": researcher.get('reason_body_1', ''),
            "Reason 2 Title / 理由2 タイトル": researcher.get('reason_title_2', ''),
            "Reason 2 Body / 理由2 詳細": researcher.get('reason_body_2', ''),
            "Reason 3 Title / 理由3 タイトル": researcher.get('reason_title_3', ''),
            "Reason 3 Body / 理由3 詳細": researcher.get('reason_body_3', '')
        })
    
    # DataFrameを作成
    df = pd.DataFrame(csv_data)
    
    # CSVファイルとして出力
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    
    return csv_buffer.getvalue()

# 🔧 動的プレースホルダー生成関数（多言語対応）
def get_dynamic_placeholder():
    """会話の文脈に基づいて次に入力される可能性の高い内容を提案"""
    
    # 初回または履歴が少ない場合
    if len(st.session_state.chat_history) <= 1:
        if st.session_state.language == "日本語":
            return "例：機械学習を使った医療診断の研究者を探しています"
        else:
            return "Example: Looking for researchers in machine learning for medical diagnosis"
    
    # 最新のエージェント応答を分析
    last_assistant_message = None
    for msg in reversed(st.session_state.chat_history):
        if msg["role"] == "assistant":
            last_assistant_message = msg["content"]
            break
    
    if not last_assistant_message:
        return get_text("input_placeholder")
    
    # エージェントの応答内容に基づいてプレースホルダーを決定
    content_lower = last_assistant_message.lower()
    
    # 日本語プレースホルダー
    if st.session_state.language == "日本語":
        # 研究分野に関する質問の場合
        if any(keyword in content_lower for keyword in ["研究分野", "分野", "どのような研究", "research field"]):
            return "例：人工知能、バイオテクノロジー、材料科学など"
        
        # 技術課題に関する質問の場合
        if any(keyword in content_lower for keyword in ["技術課題", "課題", "問題", "challenge"]):
            return "例：画像認識の精度向上、新材料の開発、診断アルゴリズムの改善など"
        
        # 予算に関する質問の場合
        if any(keyword in content_lower for keyword in ["予算", "費用", "コスト", "budget", "cost"]):
            return "例：年間500万円、プロジェクト全体で2000万円など"
        
        # 期間に関する質問の場合
        if any(keyword in content_lower for keyword in ["期間", "時間", "いつまで", "timeline", "期限"]):
            return "例：2年間、2025年まで、来年度中にはなど"
        
        # 協業タイプに関する質問の場合
        if any(keyword in content_lower for keyword in ["協業", "共同研究", "連携", "collaboration"]):
            return "例：共同研究、技術移転、コンサルティング、ライセンス契約など"
        
        # 応用分野に関する質問の場合
        if any(keyword in content_lower for keyword in ["応用", "活用", "使用", "適用", "application"]):
            return "例：医療診断、自動運転、創薬、製造業での品質管理など"
        
        # 具体的な技術について聞かれた場合
        if any(keyword in content_lower for keyword in ["機械学習", "ai", "人工知能"]):
            return "例：深層学習を用いた画像解析、自然言語処理による文書分析など"
        
        if any(keyword in content_lower for keyword in ["医療", "診断", "医学"]):
            return "例：CT画像診断、病理画像解析、遺伝子解析など"
        
        # 詳細情報を求められた場合
        if any(keyword in content_lower for keyword in ["詳しく", "具体的", "詳細", "more detail"]):
            return "例：具体的な技術要件、想定する精度、対象となるデータサイズなど"
        
        # 検索を提案された場合
        if any(keyword in content_lower for keyword in ["検索", "探し", "お探し", "search"]):
            return "例：はい、お願いします / もう少し条件を絞りたいです"
        
        # 研究者が提示された後
        if any(keyword in content_lower for keyword in ["研究者", "候補", "おすすめ"]):
            return "例：詳細を教えてください / 他の候補も見たいです / 連絡方法を教えてください"
        
        return "続きをお聞かせください"
    
    else:  # English プレースホルダー
        # Research field questions
        if any(keyword in content_lower for keyword in ["research field", "field", "what kind of research"]):
            return "Example: artificial intelligence, biotechnology, materials science, etc."
        
        # Technical challenge questions
        if any(keyword in content_lower for keyword in ["technical challenge", "challenge", "problem"]):
            return "Example: improving image recognition accuracy, developing new materials, etc."
        
        # Budget questions
        if any(keyword in content_lower for keyword in ["budget", "cost", "funding"]):
            return "Example: $500K annually, $2M for the entire project, etc."
        
        # Timeline questions
        if any(keyword in content_lower for keyword in ["timeline", "period", "deadline", "when"]):
            return "Example: 2 years, by 2025, within this fiscal year, etc."
        
        # Collaboration type questions
        if any(keyword in content_lower for keyword in ["collaboration", "partnership", "cooperation"]):
            return "Example: joint research, technology transfer, consulting, licensing, etc."
        
        # Application field questions
        if any(keyword in content_lower for keyword in ["application", "use", "implementation"]):
            return "Example: medical diagnosis, autonomous driving, drug discovery, etc."
        
        # Specific technology questions
        if any(keyword in content_lower for keyword in ["machine learning", "ai", "artificial intelligence"]):
            return "Example: deep learning for image analysis, NLP for document analysis, etc."
        
        if any(keyword in content_lower for keyword in ["medical", "diagnosis", "healthcare"]):
            return "Example: CT image diagnosis, pathology image analysis, genetic analysis, etc."
        
        # Detail requests
        if any(keyword in content_lower for keyword in ["details", "specific", "more information"]):
            return "Example: specific technical requirements, expected accuracy, data size, etc."
        
        # Search suggestions
        if any(keyword in content_lower for keyword in ["search", "find", "look for"]):
            return "Example: Yes, please proceed / I'd like to narrow down the criteria"
        
        # After researchers presented
        if any(keyword in content_lower for keyword in ["researcher", "candidate", "recommendation"]):
            return "Example: Please tell me more details / I'd like to see other candidates"
        
        return "Please continue..."

# セッション状態の初期化
if 'chat_history' not in st.session_state:
    if st.session_state.language == "日本語":
        initial_content = "こんにちは！研Q対話型エージェントです。🎓\n\n企業様の研究ニーズに最適な海外研究者をお探しいたします。以下についてお聞かせください：\n\n• どのような研究分野に興味がありますか？\n• 具体的な技術課題はありますか？\n• 協業の目的（共同研究、技術移転、コンサルティングなど）\n• 予算規模や期間のご希望\n\n何でもお気軽にご質問ください！"
    else:
        initial_content = "Hello! Welcome to KenQ Chat Agent. 🎓\n\nWe help you find the best overseas researchers for your corporate research needs. Please tell us about:\n\n• What research fields are you interested in?\n• What specific technical challenges do you have?\n• Collaboration objectives (joint research, technology transfer, consulting, etc.)\n• Budget and timeline preferences\n\nFeel free to ask any questions!"
        
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": initial_content,
            "timestamp": datetime.now().isoformat(),
            "researchers": []
        }
    ]

if 'user_context' not in st.session_state:
    st.session_state.user_context = {
        "research_field": "",
        "technical_challenge": "",
        "collaboration_type": "",
        "budget_range": "",
        "timeline": "",
        "company_info": ""
    }

# 🔧 改修①: 研究者数選択の初期化
if 'max_researchers' not in st.session_state:
    st.session_state.max_researchers = 3

# メッセージ送信カウンター（入力クリア用）
if 'message_counter' not in st.session_state:
    st.session_state.message_counter = 0

def call_backend_api(query, context=None, max_researchers=3):
    """バックエンドAPIを呼び出して研究者検索と対話応答を取得"""
    api_url = f"{API_BASE_URL}/api/chat"
    
    # JSONシリアライズ可能な形式に変換
    serializable_history = []
    for item in st.session_state.chat_history[-5:]:
        serializable_item = {
            "role": item["role"],
            "content": item["content"]
        }
        serializable_history.append(serializable_item)
    
    payload = {
        "message": query,
        "context": context or st.session_state.user_context,
        "chat_history": serializable_history,
        "max_researchers": max_researchers  # 🔧 改修①: 研究者数を送信
    }
    
    try:
        with st.spinner('APIに接続中...'):
            response = requests.post(
                api_url, 
                json=payload, 
                timeout=45,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json()
    except requests.exceptions.Timeout:
        st.error("⏰ APIの応答がタイムアウトしました。しばらく待ってから再度お試しください。")
        return {
            "response": "申し訳ございません。現在システムの応答が遅くなっております。しばらく経ってからお試しください。",
            "researchers": [],
            "context_update": {}
        }
    except requests.exceptions.ConnectionError:
        st.error("🔌 APIサーバーに接続できません。ネットワーク接続を確認してください。")
        return {
            "response": "申し訳ございません。現在システムに接続できません。しばらく経ってからお試しください。",
            "researchers": [],
            "context_update": {}
        }
    except requests.exceptions.HTTPError as e:
        st.error(f"🚨 APIエラーが発生しました (HTTP {e.response.status_code})")
        return {
            "response": f"システムエラーが発生しました。エラーコード: {e.response.status_code}",
            "researchers": [],
            "context_update": {}
        }
    except requests.exceptions.RequestException as e:
        st.error(f"❌ APIリクエストエラー: {str(e)}")
        return {
            "response": "申し訳ございません。現在システムに問題が発生しております。しばらく経ってからお試しください。",
            "researchers": [],
            "context_update": {}
        }
    except json.JSONDecodeError:
        st.error("📄 APIからの応答が正しくありません。")
        return {
            "response": "システムからの応答に問題がありました。管理者にお問い合わせください。",
            "researchers": [],
            "context_update": {}
        }

def display_chat_history():
    """チャット履歴を表示（多言語対応）"""
    st.markdown(f"### {get_text('chat_history')}")
    
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])

def display_researchers(researchers):
    """🔧 改修②: 理由表示方法を改善した研究者リスト表示（多言語対応）"""
    if not researchers:
        return
    
    st.markdown(f"### {get_text('recommended_researchers')}")
    
    # 🔧 改修機能2: CSVダウンロードボタンを追加
    if researchers:
        csv_data = create_csv_from_researchers(researchers)
        if csv_data:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"researchers_{current_time}.csv"
            
            st.download_button(
                label=f"{get_text('csv_download')} {get_text('download_csv')}",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                help=f"Download {len(researchers)} researchers data as CSV"
            )
    
    for i, researcher in enumerate(researchers, 1):
        with st.expander(f"👨‍🔬 {researcher.get('name', 'No Name')} ({researcher.get('institution', 'N/A')})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**{get_text('institution')}** {researcher.get('institution', 'N/A')}")
                st.markdown(f"**{get_text('research_field')}** {researcher.get('classified_field', 'N/A')}")
                
                orcid_url = researcher.get("orcid", "").strip()
                if orcid_url and orcid_url != "N/A":
                    if not orcid_url.startswith("http"):
                        orcid_url = f"https://orcid.org/{orcid_url}"
                    st.markdown(f"**{get_text('orcid')}** [{orcid_url}]({orcid_url})")
            
            with col2:
                st.metric(get_text('papers'), f"{researcher.get('works_count', 0):,}")
                st.metric(get_text('citations'), f"{researcher.get('cited_by_count', 0):,}")
                st.metric(get_text('h_index'), researcher.get('h_index', 0))
            
            # 🔧 改修②: おすすめ理由の表示方法を改善
            st.markdown("---")
            st.markdown(f"**{get_text('reason_title')}**")
            
            reason_displayed = False
            for j in range(1, 4):
                title = researcher.get(f"reason_title_{j}", "").strip()
                body = researcher.get(f"reason_body_{j}", "").strip()
                
                if title and body:
                    # 理由番号とタイトルを目立たせる
                    st.markdown(f"### {j}. {title}")
                    
                    # 本文を読みやすく表示
                    st.markdown(f"<div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #007acc;'>{body}</div>", unsafe_allow_html=True)
                    
                    reason_displayed = True
                elif title:
                    # タイトルのみの場合
                    st.markdown(f"### {j}. {title}")
                    reason_displayed = True
            
            if not reason_displayed:
                st.info(get_text('reason_generating'))

# メインのチャットインターフェース
display_chat_history()

# 最新の研究者提案を表示
if st.session_state.chat_history and st.session_state.chat_history[-1].get("researchers"):
    display_researchers(st.session_state.chat_history[-1]["researchers"])

# 🔧 動的プレースホルダー対応の入力フィールド
st.markdown("---")

# 🔧 改修①: 研究者数選択プルダウンを追加（多言語対応）
col_setting1, col_setting2 = st.columns([2, 3])
with col_setting1:
    max_researchers = st.selectbox(
        get_text('researcher_count'),
        options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        index=2,  # デフォルトは3名
        key="max_researchers_selector"
    )
    st.session_state.max_researchers = max_researchers

with col_setting2:
    st.markdown(f"**{get_text('current_setting')}** {max_researchers}{get_text('researchers_display')}")

# 動的プレースホルダーを取得
dynamic_placeholder = get_dynamic_placeholder()

# カウンターベースの入力クリア方式
user_input = st.text_input(
    get_text('input_placeholder'),
    placeholder=dynamic_placeholder,
    key=f"user_input_{st.session_state.message_counter}"
)

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    send_button = st.button(get_text('send_button'), type="primary")
with col2:
    test_connection = st.button(get_text('test_connection'), type="secondary")

# 接続テスト機能
if test_connection:
    try:
        test_url = f"{API_BASE_URL}/api/health"
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            st.success(get_text('connection_success'))
            health_data = response.json()
            st.json(health_data)
        else:
            st.error(f"❌ APIサーバーが正常に応答していません (Status: {response.status_code})")
    except Exception as e:
        st.error(f"{get_text('connection_failed')} {str(e)}")

# メッセージ送信処理
if send_button and user_input.strip():
    # ユーザーメッセージを追加
    st.session_state.chat_history.append({
        "role": "user", 
        "content": user_input,
        "timestamp": datetime.now().isoformat(),
        "researchers": []
    })
    
    # 🔧 改修①: 研究者数を含めてAPIを呼び出し
    api_response = call_backend_api(
        user_input, 
        st.session_state.user_context,
        max_researchers=st.session_state.max_researchers
    )
    
    # エージェントの応答を追加
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": api_response.get("response", "申し訳ございません。応答の生成に失敗しました。"),
        "timestamp": datetime.now().isoformat(),
        "researchers": api_response.get("researchers", [])
    })
    
    # ユーザーコンテキストを更新
    if api_response.get("context_update"):
        st.session_state.user_context.update(api_response["context_update"])
    
    # メッセージカウンターを増加（新しい入力フィールドを生成）
    st.session_state.message_counter += 1
    
    st.rerun()

# サイドバー - システム情報とコンテキスト（多言語対応）
with st.sidebar:
    st.markdown(f"## {get_text('system_info')}")
    st.markdown(f"**API URL:** {API_BASE_URL}")
    st.markdown("**バージョン:** 4.4.0 (多言語対応＆CSVダウンロード)")
    
    # API状態表示
    try:
        health_response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        if health_response.status_code == 200:
            st.success("🟢 API Online")
        else:
            st.error("🔴 API Error")
    except:
        st.error("🔴 API Offline")
    
    st.markdown("---")
    st.markdown(f"## {get_text('display_settings')}")
    st.markdown(f"**{get_text('researcher_count').replace(':', '')}:** {st.session_state.max_researchers}名")
    st.markdown(f"**Language / 言語:** {st.session_state.language}")
    
    st.markdown("---")
    st.markdown(f"## {get_text('context_info')}")
    
    context_items = [
        ("研究分野", st.session_state.user_context.get("research_field", "")),
        ("技術課題", st.session_state.user_context.get("technical_challenge", "")),
        ("協業タイプ", st.session_state.user_context.get("collaboration_type", "")),
        ("予算規模", st.session_state.user_context.get("budget_range", "")),
        ("期間", st.session_state.user_context.get("timeline", ""))
    ]
    
    for label, value in context_items:
        if value:
            st.markdown(f"**{label}:** {value}")
    
    # チャットリセット
    if st.button(get_text('reset_chat'), type="secondary"):
        # 初期メッセージを言語に応じて設定
        if st.session_state.language == "日本語":
            initial_message = "こんにちは！研Q対話型エージェントです。🎓\n\n企業様の研究ニーズに最適な海外研究者をお探しいたします。何でもお気軽にご質問ください！"
        else:
            initial_message = "Hello! Welcome to KenQ Chat Agent. 🎓\n\nWe help you find the best overseas researchers for your corporate research needs. Please feel free to ask any questions!"
        
        st.session_state.chat_history = [{
            "role": "assistant",
            "content": initial_message,
            "timestamp": datetime.now().isoformat(),
            "researchers": []
        }]
        st.session_state.user_context = {
            "research_field": "",
            "technical_challenge": "",
            "collaboration_type": "",
            "budget_range": "",
            "timeline": "",
            "company_info": ""
        }
        # カウンターリセットで入力フィールドも新しく生成
        st.session_state.message_counter += 1
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"## {get_text('placeholder_function')}")
    st.markdown(f"**現在の提案:** {dynamic_placeholder[:50]}...")
    if st.session_state.language == "日本語":
        st.caption("会話の流れに応じて入力例が自動で変わります")
    else:
        st.caption("Input examples change automatically based on conversation flow")
    
    st.markdown("---")
    st.markdown(f"## {get_text('usage_tips')}")
    if st.session_state.language == "日本語":
        st.markdown("""
        - 研究分野や技術課題を具体的に
        - 協業の目的を明確に
        - 予算や期間の希望があれば
        - 企業の業界や規模も参考になります
        """)
    else:
        st.markdown("""
        - Be specific about research fields and technical challenges
        - Clarify collaboration objectives
        - Include budget and timeline preferences if available
        - Company industry and size information is also helpful
        """)
    
    st.markdown("---")
    st.markdown(f"## {get_text('debug_info')}")
    with st.expander("詳細情報" if st.session_state.language == "日本語" else "Details"):
        st.json({
            "API_BASE_URL": API_BASE_URL,
            "chat_history_length": len(st.session_state.chat_history),
            "context_keys": list(st.session_state.user_context.keys()),
            "current_placeholder": dynamic_placeholder,
            "message_counter": st.session_state.message_counter,
            "max_researchers": st.session_state.max_researchers,
            "language": st.session_state.language
        })