# -*- coding: utf-8 -*-
import subprocess

server = "RTX3070TI\TEST1"
database = "master"
user = "sa"
password = "sa"
port = "1433"
table = "table2"
batch_size = 1000 # 後で使用する

csv_file = r"out.tsv"


# -b {batch_size}  # 一括インポートする行数
# -c               # フィールドの確認画面なし
# -C 65001         # データの文字コードを　「UTF-8」 に設定する
# -a 32784         # パケットバイト数を 「32784」 に設定
# -t ','           # CSVファイルの区切り文字を「カンマ」に指定
# # もしCSVファイルのヘッダーがある場合はこのようにする
# -F 2             # 上から2行目から値のインポートを始める

# BCPコマンドを用意
bcp = 'bcp {table} in "{csv_file}" -S {server} -U {user} -P {password} -d {database} -b {batch_size} -c -C 65001 -a 32784 '.format(
    table=table,
    csv_file=csv_file,
    server=server,
    user=user,
    password=password,
    database=database,
    batch_size=batch_size
)
print(bcp)
subprocess.run(bcp, shell=True)