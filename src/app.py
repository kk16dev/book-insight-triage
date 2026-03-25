"""
Streamlitフロントエンド - 本のメモ分析チャットUI
"""
import streamlit as st
from ai_processor import BookInsightProcessor


def initialize_session_state():
    """セッションステートの初期化"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "processor" not in st.session_state:
        st.session_state.processor = None


def initialize_processor():
    """AI Processorの初期化"""
    try:
        if st.session_state.processor is None:
            with st.spinner("AI プロセッサを初期化中..."):
                st.session_state.processor = BookInsightProcessor()
            st.success("AI プロセッサの初期化が完了しました")
        return True
    except Exception as e:
        st.error(f"AI プロセッサの初期化に失敗しました: {str(e)}")
        st.info("AWS認証情報が正しく設定されているか確認してください")
        return False


def main():
    """メインアプリケーション"""
    st.set_page_config(
        page_title="Book Insight Triage",
        page_icon="📚",
        layout="wide"
    )

    st.title("📚 Book Insight Triage")
    st.markdown("本のメモから**事実**、**意見**、**今日から取り組めること**を整理します")

    # セッションステートの初期化
    initialize_session_state()

    # サイドバー
    with st.sidebar:
        st.header("⚙️ 設定")

        # プロセッサの初期化ボタン
        if st.button("🔄 プロセッサを初期化", use_container_width=True):
            st.session_state.processor = None
            initialize_processor()

        # モデル情報の表示
        if st.session_state.processor:
            st.divider()
            st.subheader("モデル情報")
            model_info = st.session_state.processor.get_model_info()
            st.text(f"モデル: {model_info['model_id']}")
            st.text(f"リージョン: {model_info['region']}")

        st.divider()
        st.subheader("使い方")
        st.markdown("""
        1. 本のメモをテキストエリアに入力
        2. 「分析」ボタンをクリック
        3. AIが事実・意見・行動を整理
        """)

        # 会話履歴のクリア
        if st.button("🗑️ 会話履歴をクリア", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # メインエリア
    # プロセッサの初期化チェック
    if not st.session_state.processor:
        if not initialize_processor():
            st.stop()

    # 会話履歴の表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ユーザー入力
    st.divider()
    st.subheader("📝 本のメモを入力")

    with st.form("memo_form", clear_on_submit=True):
        memo = st.text_area(
            "メモの内容",
            height=200,
            placeholder="本のメモをここに入力してください...\n\n例:\n・習慣は小さく始めることが重要\n・著者は2分ルールを推奨している\n・習慣化には平均66日かかる研究結果がある"
        )

        submitted = st.form_submit_button("📊 分析", use_container_width=True)

        if submitted and memo:
            # ユーザーメッセージを追加
            st.session_state.messages.append({
                "role": "user",
                "content": memo
            })

            # ユーザーメッセージを表示
            with st.chat_message("user"):
                st.markdown(memo)

            # AI処理
            with st.chat_message("assistant"):
                with st.spinner("分析中..."):
                    try:
                        response = st.session_state.processor.process_memo(memo)
                        st.markdown(response)

                        # アシスタントメッセージを追加
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response
                        })
                    except Exception as e:
                        error_msg = f"エラーが発生しました: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })


if __name__ == "__main__":
    main()
