

import requests 
# SharePointのExcelファイルのURL 
url = 'https://yourtenant.sharepoint.com/sites/yoursite/Shared%20Documents/yourfile.xlsx' 

# 認証情報（必要に応じて変更） 
username = 'your_username' 
password = 'your_password' 

# セッションを作成 
session = requests.Session() 
session.auth = (username, password) 
response = session.get(url) 



import requests
from requests_ntlm import HttpNtlmAuth

# SharePointのExcelファイルのURL
url = 'https://yourtenant.sharepoint.com/sites/yoursite/Shared%20Documents/yourfile.xlsx'

# Windows認証用のユーザー名とパスワード
username = 'domain\\your_username'  # ドメイン名とユーザー名を指定
password = 'your_password'

# セッションを作成
session = requests.Session()
session.auth = HttpNtlmAuth(username, password)

# Excelファイルを取得
response = session.get(url)

# ステータスコードの確認
if response.status_code == 200:
    # ファイルが正常に取得できた場合
    with open('downloaded_file.xlsx', 'wb') as file:
        file.write(response.content)
    print("ファイルが正常にダウンロードされました。")
else:
    print(f"エラーが発生しました: {response.status_code}")