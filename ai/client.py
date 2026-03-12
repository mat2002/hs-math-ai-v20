import os
from openai import OpenAI

def get_openai_client():
    """
    OpenAI クライアントを取得する。
    環境変数 OPENAI_API_KEY が設定されていない場合は、Manus のデフォルトキーを使用する。
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        # Render 等の環境で API キーが設定されていない場合、
        # ビルド時のインポートエラーを避けるためにダミーのキーを返す。
        # 実際に API を呼び出す際にはエラーになるが、起動は可能になる。
        return OpenAI(api_key="sk-no-key-provided-please-set-env-var")

    return OpenAI(api_key=api_key)

# クラスとして定義し、プロパティでアクセスすることで初期化を遅延させる
class OpenAIClientProxy:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = get_openai_client()
        return self._client

    def __getattr__(self, name):
        return getattr(self.client, name)

# シングルトンインスタンス
client = OpenAIClientProxy()
