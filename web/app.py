from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>高校数学教材AI v20 - Web UI</title>
        <style>
            body { font-family: sans-serif; margin: 40px; line-height: 1.6; }
            .container { max-width: 800px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
            h1 { color: #2c3e50; }
            .status { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>高校数学教材AI v20</h1>
            <p>Web UI サーバーが正常に起動しました。</p>
            <p class="status">ステータス: 稼働中</p>
            <hr>
            <h3>教材生成メニュー</h3>
            <ul>
                <li>演習プリント生成</li>
                <li>小テスト生成</li>
                <li>模試生成</li>
                <li>教科書生成</li>
            </ul>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    # 外部からのアクセスを許可するため 0.0.0.0 で起動
    app.run(host='0.0.0.0', port=5000)
