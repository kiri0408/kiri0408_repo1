
import win32com.client
import os
import polars as pl
import numpy as np
import sys
filepath=r'C:\py\99.sonota\df_4.xlsx'
filename=os.path.basename(filepath)
sheetname='Sheet3'
#max_col = 600

try:
    #EXCELオープン
    xl = win32com.client.GetObject(Class="Excel.Application")
    wb = xl.Workbooks(filename)
    ws = wb.Sheets(sheetname)
    xl.DisplayAlerts = False # 警告を非表示
except:
    print("エラー発生しました")
    xl.DisplayAlerts = True # 警告を表示



# ws から  列名とデータを取得
row_end = ws.Cells(ws.Rows.Count, 3).End(-4162).Row   #  最終行取得  xlUp = -4162   # VBAで"xlUp"を示す定数
col_end = 100
tpl_columns = ws.Range(ws.cells(1,1),ws.cells(1,col_end)).value 
tpl_data    = ws.Range(ws.cells(2,1),ws.cells(row_end,col_end)).value 

# 列名の空白はcol?で埋めてリスト型に変換
list_columns = list(tpl_columns[0])
for i in range(len(list_columns)):
    if list_columns[i] == None:
        list_columns[i] = 'col'+str(i+1)

#Dataframeへ変換
df = pl.DataFrame(np.array(tpl_data))
try:
    df.columns = list_columns
except:
    print(list_columns)
    print('Error:列名に重複が無いか確認願います')
    sys.exit()

#数値型の列はObjectから数値型へ変換
df = df.with_columns(pl.col('tankaD').apply(float))   #数値でない場合はNULLにする関数の方がいい
print(df)

#特定のカラム名の列番号を取得し、ws更新
column_name = "単価c"
column_index = df.columns.index(column_name)
print(f"列名 '{column_name}' の列番号は: {column_index}")
ws.cells(8,column_index+1).Value = 41.0

np_array = df['単価c'].to_numpy()  #カラム指定でデータを取り出す
np_array = np_array.reshape(-1,1)  #カラム１列分なので、縦一列に変換する  
_tuple = tuple(np_array)

#ws.Range(ws.cells(20,2),ws.cells(20,10)).Value = _tuple
col_out = 2
datasize = len(_tuple)
ws.Range(ws.cells(2,col_out),ws.cells(2 + datasize -1 ,col_out)).Value = _tuple


xl.DisplayAlerts = True # 警告を表示
print('end')