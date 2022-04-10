from win32com.client import GetObject
import pythoncom

#https://qiita.com/feo52/items/150745ae0cc17cb5c866

xl = GetObject(None, "Excel.Application")
xl.Visible = True  # ビジブル設定
xl.DisplayAlerts = False # 警告を非表示

wb = xl.Workbooks("test1.xlsx")
ws = wb.Sheets("bbb")
ws2 = wb.sheets("aaa")

#セル値を2次元配列で取得：タプルで取得される
ary1 = ws.Range(ws.cells(1,1),ws.cells(10000,100)).Value
#print(f"{ary1=}")

ws2.Range(ws2.cells(1,1),ws2.cells(10000,100)).Value = ary1

ws.Range("A1:B4").Value = "値"

# A1からB列最終行まで一括して同じ値を入力
#ws.Range(f"A1:B{endRow}").Value = "値"
ws.Range(ws.Cells(1, 1), ws.Cells(30, 2)).Value = "値"

xlUp = -4162   # VBAで"xlUp"を示す定数
endRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
print(endRow)

#セルにExcel関数を代入したい場合は.Formulaを使います
ws.Range("A11").Formula = "=SUM(A1:A10)"

#罫線
ws.Range("A11:H11").Borders(9).LineStyle = 1  #xlEdgeBottom=9 下線 xlContinuous=1 実線
ws.Range("A11:H11").Borders(9).Weight = -4138     #xlMedium=-4138 普通の太さ
ws.Range("A11:H11").Borders(9).ColorIndex = -4105  #-4105自動

ws.Range("D11:F11").Borders(9).LineStyle = -4142  #xlLineStyleNone	-4142	線なし

#セルの表示書式
ws.Range("A11").value = "2022/04/01"
ws.Range("A11").NumberFormatLocal = "yyyy/mm/dd" 
ws.Range("A11").NumberFormatLocal = "m/d" 

# A1セルの背景の色を設定(指定順序BGR)
ws.Range("A1:H1").Interior.Color = int("FFFF00",16)

# A1セルの背景の色を設定(デフォルト)
ws.Range("C1").Interior.ColorIndex = -4142  # xlColorIndexNone      = -4142 


# A1セルの値や数式を消去
ws.Range("A1").ClearContents()

# A1セルの書式を消去
ws.Range("A1").ClearFormats()

# A1セルを消去
ws.Range("A1").Clear()

# (A1行基準で)高さを設定
ws.Range("B2").RowHeight = 30

    # 列のグループ化を設定
ws.Range("B2").EntireColumn.Group()

    # 列のグループ化を解除
ws.Range("B2").EntireColumn.Ungroup()


# AutoFilterの解除
if ws.AutoFilterMode:
    ws.AutoFilterMode = False

# A1セル基準の現在の領域をAutoFilter
ws.Range("B1").AutoFilter()

# AutoFilterの適用
ws.AutoFilter.ApplyFilter()

# AutoFilterの絞り込み解除
if ws.FilterMode:
    ws.ShowAllData()

# 枠の固定
ws.Activate()
xl.ActiveWindow.FreezePanes = False
ws.Range("C2").Select()
xl.ActiveWindow.FreezePanes = True


import pandas as pd

df = pd.read_excel('data1.xlsx')
print(df)

_tuple = [tuple(x) for x in df.values] #dfをタプルへ変換

ws2.Range(ws2.cells(10,10),ws2.cells(13,12)).Value = _tuple

print('end')

# 終了処理
pythoncom.CoInitialize() 