# coding: utf-8

import pyodbc

DB = {'servername': "RTX3070TI\TEST1" ,   'database': 'master'}

import csv

file_name = "upd.tsv"

data =[]
with open(file_name, "r", encoding="utf-8", newline="") as f:
	# 読み込み（リーダーを取得）
	rs = csv.reader(f, delimiter="\t")
	# 1行ずつループ
	for r in rs:
		data.append(tuple(r))


# DB検索 
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + DB['servername'] + ';DATABASE=' + DB['database'] + ';Trusted_Connection=yes')

# カーソルを定義
cursor = conn.cursor()

#print('一旦クリア')
#cursor.execute("delete  from table2 where keycode in ( select keycode from table1 ) ")  #一旦クリア

# クエスチョンパラメータにしたSQL文を用意
sql = "update table2 set keikaku_bi = ?  where keycode = ?  and kotei_cd = ? ;"

cursor.fast_executemany = True # 高速でexecutemanyを行うための呪文
batch_size = 1000 # 1回でデータを入れる量


# 全てのデータを、バッチサイズで区切ってSQLを実行する。
for i in range(0, len(data), batch_size):
    print(i)
    cursor.executemany(sql, data[i : i + batch_size])

    # コミットしてデータを反映させる
    cursor.commit()

# コネクションを閉じる
cursor.close()
conn.close()


