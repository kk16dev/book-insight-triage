# 📚 Book Insight Triage

本のメモから**事実**、**意見**、**今日から取り組めること**を整理するツールです。

## 🎯 機能

- 本のメモをAIが自動分析
- 以下の3つの観点で整理:
  - 📋 **事実**: 客観的な情報、データ、研究結果
  - 💭 **意見**: 著者の主張、解釈、推奨事項
  - ✅ **今日から取り組めること**: 実践できる具体的なアクション

## 🛠️ 技術スタック

- **フロントエンド**: Streamlit
- **AI処理**: LangChain + AWS Bedrock
- **パッケージ管理**: uv

## 📋 前提条件

- Python 3.13以上
- AWS アカウントと Bedrock へのアクセス権限
- AWS CLI の設定が完了していること

## 🚀 セットアップ

### 1. リポジトリのクローン

```bash
cd /home/kk/tool/book-insight-triage
```

### 2. 依存関係のインストール

```bash
uv sync
```

### 3. AWS認証情報の設定

AWS CLIで認証情報を設定します。

```bash
aws configure
```

### 4. AWS Bedrock モデルへのアクセス確認

AWS コンソールで以下を確認:
1. Bedrock サービスにアクセス
2. Claude 3.5 Sonnet モデルが利用可能であることを確認
3. 必要に応じてモデルアクセスをリクエスト

## 💻 使い方

### アプリケーションの起動

```bash
uv run streamlit run src/app.py
```

ブラウザが自動的に開き、アプリケーションが表示されます（通常は http://localhost:8501）。

### 基本的な使い方

1. アプリケーションが起動したら、テキストエリアに本のメモを入力
2. 「📊 分析」ボタンをクリック
3. AIが自動的に分析して、事実・意見・今日から取り組めることを整理

### メモの入力例

```
『アトミック・ハビッツ』より:

・習慣は複利のように積み重なる
・1%の改善を毎日続けると1年で37倍になる
・著者は2分ルールを推奨: 新しい習慣は2分以内でできることから始める
・習慣の4つの法則: はっきりさせる、魅力的にする、易しくする、満足できるものにする
・環境設計が習慣形成に重要
・ロンドン大学の研究では習慣化には平均66日かかる
```

## 📁 プロジェクト構造

```
book-insight-triage/
├── README.md              # このファイル
├── pyproject.toml         # プロジェクト設定
├── .env.example           # 環境変数の例
├── .gitignore            # Git除外設定
└── src/
    ├── app.py            # Streamlit フロントエンド
    └── ai_processor.py   # LangChain + Bedrock AI処理
```

## 🔧 カスタマイズ

### モデルの変更

`src/ai_processor.py` の `BookInsightProcessor` クラスでモデルを変更できます:

```python
processor = BookInsightProcessor(
    model_id="jp.amazon.nova-2-lite-v1:0",  # モデルID
    region_name="ap-northeast-1"  # リージョン
)
```

### プロンプトのカスタマイズ

`src/ai_processor.py` の `system_prompt` を編集して、分析の観点や出力形式を変更できます。

## 🐛 トラブルシューティング

### AWS認証エラー

```
AI プロセッサの初期化に失敗しました
```

**解決方法**:
1. AWS CLI が正しく設定されているか確認: `aws sts get-caller-identity`
2. Bedrock へのアクセス権限があるか確認
3. リージョンが正しいか確認（Bedrock が利用可能なリージョン）

### モデルアクセスエラー

```
Model access denied
```

**解決方法**:
1. AWS コンソール → Bedrock → Model access
2. Claude モデルへのアクセスをリクエスト
3. 承認されるまで待機（通常は即時）

## 📝 ライセンス

このプロジェクトは個人利用を目的としています。

## 🤝 貢献

バグ報告や機能リクエストは Issue にてお願いします。
