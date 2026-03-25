"""
AI処理モジュール - LangChain + AWS Bedrockを使用して本のメモを分析
"""
from typing import Dict
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage


class BookInsightProcessor:
    """本のメモから事実、意見、行動を抽出するプロセッサ"""

    def __init__(
        self,
        model_id: str = "jp.amazon.nova-2-lite-v1:0",
        region_name: str = "ap-northeast-1"
    ):
        """
        初期化

        Args:
            model_id: 使用するBedrockモデルID
            region_name: AWSリージョン
        """
        self.llm = ChatBedrock(
            model_id=model_id,
            region_name=region_name,
            model_kwargs={
                "temperature": 0.3,
                "max_tokens": 8192,
            }
        )

        self.system_prompt = """あなたは本のメモを分析する専門家です。
ユーザーから本のメモを受け取ったら、以下の3つの観点で整理してください:

1. **事実**: 本に書かれている客観的な情報、データ、研究結果、歴史的事実など
2. **意見**: 著者の主張、解釈、推奨事項、個人的な見解など
3. **今日から取り組めること**: 読者が実践できる具体的なアクション、習慣、手法など

各カテゴリーは箇条書きで簡潔にまとめてください。
明確に区別できる形式で出力してください。

出力形式:
## 📋 事実
- ...
- ...

## 💭 意見
- ...
- ...

## ✅ 今日から取り組めること
- ...
- ...
"""

    def process_memo(self, memo: str) -> str:
        """
        本のメモを処理して、事実・意見・行動を抽出

        Args:
            memo: 本のメモ

        Returns:
            処理結果のテキスト
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"以下の本のメモを分析してください:\n\n{memo}")
        ]

        response = self.llm.invoke(messages)
        return response.content

    def get_model_info(self) -> Dict[str, str]:
        """
        使用しているモデル情報を取得

        Returns:
            モデル情報の辞書
        """
        return {
            "model_id": self.llm.model_id,
            "region": self.llm.region_name,
        }
