@echo off
setlocal
cd /d %~dp0

echo 高校数学教材AI v20 を起動しています...
echo.

:: 仮想環境の存在確認
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] 仮想環境 (venv) が見つかりません。
    echo ターミナルで 'python -m venv venv' を実行して作成してください。
    pause
    exit /b
)

:: 仮想環境を有効化
call venv\Scripts\activate.bat

:: 環境変数を設定
set FLASK_APP=web/app.py
set FLASK_ENV=development

:: ブラウザで自動的に開く (少し待ってから)
start http://127.0.0.1:5000

:: Flaskを起動
echo.
echo サーバーを起動しました。ブラウザで http://127.0.0.1:5000 を開いています。
echo この画面を閉じるとアプリが停止します。
echo.
python -m flask run

pause
endlocal
