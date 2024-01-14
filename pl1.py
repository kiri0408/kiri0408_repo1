import polars as pl

# 生産計画と部品表から引き当て情報を作成
# 納期修正処理
# 月での合計値。過去日は202312に含める
# 品目コード、月でマージ。 
# ※品目コード、202312始まりの連続月にマージすることで月の抜けをなくす。
# 現在在庫数を起点に、各月末の在庫数を計算


df = pl.read_excel('r.xlsx',sheet_name='Sheet3')
print(df)

df = df.group_by(['品目コード','年月']).sum().sort(['品目コード','年月'])
print(df)

df = df.pivot(values='払出数',index='品目コード',columns='年月',aggregate_function='sum')
print(df)

df.write_excel('a.xlsx')


df_pl = pl.read_excel('r.xlsx',sheet_name='Sheet3')
numpy_array = df_pl.to_numpy()
_tuple = tuple([tuple(e) for e in numpy_array])
print(_tuple)

import win32com.client
try:
    #EXCELオープン
    #▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽
    #xl = GetObject(None, "Excel.Application")
    xl = win32com.client.Dispatch("Excel.Application")
    from pathlib import Path
    abspath = str(Path(r"C:\py\65_r在庫\b.xlsx").resolve())
    wb = xl.Workbooks.Open(abspath, UpdateLinks=0, ReadOnly=False)  # 読み取り専用の場合は  ReadOnly=True
    ws = wb.Sheets("ws")
    xl.DisplayAlerts = False # 警告を非表示
    xl.Visible = True  #非表示
    #△△△△△△△△△△△△△△△△△△△△△△△
except:
    print("エラー発生しました")
    #EXCEL終了処理
    #▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽
    xl.DisplayAlerts = True # 警告を表示
    xl.Visible = True       # 表示
    #△△△△△△△△△△△△△△△△△△△△

try:
    #df-Excel出力 
    #▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽
    startRow = 5
    startCol = 3
    endRow = ws.Cells(ws.Rows.Count, 3).End(-4162).Row #  最終行取得  xlUp = -4162   # VBAで"xlUp"を示す定数
    endCol = 10
    ws.Range(ws.cells(startRow,startCol),ws.cells(startRow+len(_tuple)-1,endCol-1)).Value = _tuple #tuple-Excel出力
    #△△△△△△△△△△△△△△△△△△△△

except:
    print("エラー発生しました")
    #EXCEL終了処理
    #▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽
    xl.DisplayAlerts = True # 警告を表示
    xl.Visible = True       # 表示
    #△△△△△△△△△△△△△△△△△△△△
