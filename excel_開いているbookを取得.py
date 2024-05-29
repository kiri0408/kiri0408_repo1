
import win32com.client
import os
import polars as pl

filepath=r'C:\py\99.sonota\df_4.xlsx'
filename=os.path.basename(filepath)
sheetname='Sheet3'
max_col = 600

try:
    #EXCELオープン
    xl = win32com.client.GetObject(Class="Excel.Application")
    wb = xl.Workbooks(filename)
    ws = wb.Sheets(sheetname)
    
    xl.DisplayAlerts = False # 警告を非表示
    xl.Visible = False  #非表示

except:
    print("エラー発生しました")
    xl.DisplayAlerts = True # 警告を表示
    xl.Visible = True       # 表示

for j in range(1,max_col):
    if j % 100 == 0:
        print('列情報読み込み中：',j)
    if ws.cells(1,j).value == None :
        ws.cells(1,j).value = '_'

xl.DisplayAlerts = True # 警告を表示
xl.Visible = True       # 表示

wb.Save()

df = pl.read_excel(filepath,sheet_name=sheetname)
print(df)

column_name = "単価２"
column_index = df.columns.index(column_name)

print(f"列名 '{column_name}' の列番号は: {column_index}")