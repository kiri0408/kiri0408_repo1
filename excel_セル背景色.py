# coding:utf-8
import pandas as pd
import os
import win32com.client
import win32con
import win32gui

df = pd.read_excel('test.xlsx')

print(df)


# Excel起動
xlApp = win32com.client.Dispatch("Excel.Application")

# https://stackoverflow.com/questions/2790825/
# ExcelのWindow最大化
#win32gui.ShowWindow(xlApp.hwnd, win32con.SW_MAXIMIZE)

# Excel表示
xlApp.Visible = 1

# Excelファイルオープン
wb = xlApp.Workbooks.Open(f"{os.getcwd()}\\test.xlsx")

# Excelシートオブジェクト
ws = wb.Worksheets(1)


ws.Range("B2").Value = 99999
ws.Range("B2").Interior.Color = int("FFFF00",16)

