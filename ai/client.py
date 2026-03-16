import os
from openai import OpenAI

def get_openai_client():
    """
    OpenAI クライアントを取得する。
    環境変数 OPENAI_API_KEY が設定されていない場合はエラーを発生させる。
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key or api_key == "sk-no-key-provided-please-set-env-var":
        raise ValueError("OPENAI_API_KEY 環境変数が設定されていません。有効なAPIキーを設定してください。")

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
