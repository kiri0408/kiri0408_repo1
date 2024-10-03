import subprocess

# 出力するファイルパスを指定
output_file = "C:\\data\\table1_output.txt"

# SQL Server 接続設定
server_name = "localhost"   # SQL Server のサーバー名または IP アドレス
database_name = "TestDB"    # データベース名
username = "sa"             # SQL Server のユーザー名
password = "password123"    # パスワード

# 実行するSQL文を指定
query = "select hinmoku, ord, kiku from table1"

# bcp コマンドの作成
bcp_command = f'bcp "{query}" out "{output_file}" -S {server_name} -d {database_name} -U {username} -P {password} -c'

try:
    # subprocess で bcp コマンドを実行
    result = subprocess.run(bcp_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    print("bcp コマンドの実行が成功しました。")
    print("出力結果:", result.stdout)  # 標準出力を表示
except subprocess.CalledProcessError as e:
    print("bcp コマンドの実行中にエラーが発生しました。")
    print("エラーコード:", e.returncode)
    print("エラー詳細:", e.stderr)  # 標準エラー出力を表示
