# Book Insight Triage - Claude Code 開発ガイド

## 📚 プロジェクト概要

本のメモから**事実**、**意見**、**今日から取り組めること**の3つの観点で自動整理するツール。

### 主な機能
- 本のメモをAIが自動分析
- 3つの観点で構造化（事実、意見、今日から取り組めること）
- Markdown形式でダウンロード可能
- シングルターンUI（1回の分析のみ表示）

## 🛠️ 技術スタック

- **フロントエンド**: Streamlit 1.55.0+
- **AI処理**: LangChain 1.2.13+ + AWS Bedrock
- **AIモデル**: Amazon Nova 2 Lite (`jp.amazon.nova-2-lite-v1:0`)
- **パッケージ管理**: uv
- **Python**: 3.13+

## 📁 プロジェクト構造

```
book-insight-triage/
├── src/
│   ├── app.py              # Streamlitフロントエンド（UIロジック）
│   └── ai_processor.py     # LangChain + Bedrock AI処理
├── README.md               # ユーザー向けドキュメント
├── CLAUDE.md              # このファイル（開発ガイド）
├── pyproject.toml         # プロジェクト設定・依存関係
└── .gitignore
```

## 🎯 アーキテクチャ

### 責務の分離
- **src/app.py**: UI/UX、ユーザー入力、結果表示、ダウンロード機能
- **src/ai_processor.py**: AI処理、プロンプト管理、Bedrockとの通信

### データフロー
1. ユーザーが本のメモを入力
2. `BookInsightProcessor.process_memo()` で分析
3. LangChainがBedrockのNova 2 Liteを呼び出し
4. 結果を3つの観点（事実、意見、今日から取り組めること）に整理
5. Streamlitで表示 + Markdownダウンロード

## 💻 開発ガイドライン

### セットアップ

```bash
# 依存関係のインストール
uv sync

# AWS認証情報の設定（必須）
aws configure

# アプリケーション起動
uv run streamlit run src/app.py
```

### コーディング規約

1. **ファイル分割**: フロントエンドとAI処理は必ず分離
2. **型ヒント**: 関数には型ヒントを付ける
3. **Docstring**: すべての関数にDocstringを記載
4. **命名規則**:
   - 関数: `snake_case`
   - クラス: `PascalCase`
   - 定数: `UPPER_SNAKE_CASE`

### UI/UX設計原則

- **シングルターン**: 1回の分析結果のみ表示
- **シンプル**: 結果表示時は入力フォームを非表示
- **永続性**: ダウンロードボタンを押しても結果は消えない
- **リセット**: 新しい分析はブラウザ再読み込み（F5）

## 🔧 主要コンポーネント

### BookInsightProcessor (`src/ai_processor.py`)

AIプロセッサのコアクラス。

```python
processor = BookInsightProcessor(
    model_id="jp.amazon.nova-2-lite-v1:0",
    region_name="ap-northeast-1"
)
response = processor.process_memo(memo_text)
```

**重要な設定**:
- `temperature`: 0.3（一貫性重視）
- `max_tokens`: 8192
- システムプロンプト: 3つの観点での分析を指示

### Streamlit App (`src/app.py`)

UIロジックの実装。

**重要な関数**:
- `initialize_session_state()`: セッション初期化
- `initialize_processor()`: AI Processor初期化
- `show_download_button()`: ダウンロードボタン表示
- `generate_filename()`: タイムスタンプ付きファイル名生成

**状態管理**:
- `st.session_state.messages`: 分析結果の保持
- `st.session_state.processor`: AIプロセッサインスタンス

## 🐛 トラブルシューティング

### AWS Bedrock関連

**エラー**: `ValidationException: Invocation of model ID ... with on-demand throughput isn't supported`
- **原因**: クロスリージョンモデルの直接呼び出し
- **解決**: リージョン固有のモデルID（`jp.amazon.nova-2-lite-v1:0`）を使用

**エラー**: `AI プロセッサの初期化に失敗しました`
- **原因**: AWS認証情報の未設定
- **解決**: `aws configure` で認証情報を設定

### Streamlit関連

**エラー**: `st.download_button() can't be used in an st.form()`
- **原因**: formの中でdownload_buttonを使用
- **解決**: formの外で処理を実行

## 📝 コミット規約

```
<type>: <subject> (closes #issue)

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🚀 今後の開発方針

### 検討中の機能
- 複数のファイル形式でのエクスポート（PDF, JSON）
- 分析結果の履歴保存
- カスタムプロンプトの設定UI
- 他のAIモデルのサポート（Claude, GPT-4など）

### パフォーマンス最適化
- レスポンスキャッシュの導入
- ストリーミングレスポンス対応

## 🔐 セキュリティ

- `.env`ファイルは`.gitignore`に含める
- AWS認証情報はAWS CLIで管理（コードに含めない）
- APIキーや機密情報はコミットしない

## 📚 参考リンク

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Amazon Nova Models](https://aws.amazon.com/bedrock/nova/)

---

**最終更新**: 2026-03-25
