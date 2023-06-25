import pandas as pd
import win32com.client
from datetime import timedelta
import shutil
import datetime
import re
import sys

def jitudo(date, offset):
    return date + timedelta(days=offset)

def split_cell(cell):
    """「AB28」を「AB」と「28」に分けてリストで返します。"""
    column = re.search(r"[A-Z]+", cell).span()
    line = re.search(r"[0-9]+", cell).span()
    return [cell[column[0]:column[1]], cell[line[0]:line[1]]]

def convert_alphabet2num(alphabet):
    """アルファベットと数字に変換します。「AB」なら「28」に変換します。"""
    if not re.search(r"\A[A-Z]+\Z", alphabet):
        sys.exit("ERROR: '{}' is invalid value".format(alphabet))
    num = 0
    for cnt, val in enumerate(list(alphabet)):
        num += pow(26, len(alphabet) - cnt - 1)*(ord(val) - ord('A') + 1)
    return num

def convert_cell2num(cell):
    """「AB28」を数字のリストに変換します。[28, 28]が返ってきます。"""
    if not re.search(r"\A[A-Z]+[0-9]+\Z", cell):
        sys.exit("ERROR: '{}' is invalid value".format(cell))
    return [convert_alphabet2num(split_cell(cell)[0]), int(split_cell(cell)[1])]


if __name__ == "__main__":
    cell = "AB"
    print(convert_alphabet2num(cell))

    book = r'C:\py\57_excel工程表\工程表.xlsx'
    sheet ='Sheet1'

    #ファイルバックアップ
    dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    book_bk = book + dt_now + '.xlsx'
    shutil.copy2(book, book_bk)


    row_cal = 7
    col_cal = 12
    row_sta = 8 
    col_taisho = 1
    col_kenmei = 2
    col_kubun = 3
    col_date1 = 4
    col_date2 = 5
    col_date3 = 6
    col_date4 = 7
    col_bumon = 11
    col_end = 91

    #df_kotei = pd.read_excel(book,sheet_name=sheet)

    try:
        #EXCELオープン
        #▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽
        #xl = GetObject(None, "Excel.Application")
        xl = win32com.client.Dispatch("Excel.Application")
        from pathlib import Path
        abspath = str(Path(book).resolve())
        wb = xl.Workbooks.Open(abspath, UpdateLinks=0, ReadOnly=False)  # 読み取り専用の場合は  ReadOnly=True
        ws = wb.Sheets(sheet)
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

    print(ws.cells(7,2).value)
    ws.cells(6,2).value ='aaa'

    date_sta = ws.cells(row_cal,col_cal).value
    date2 = jitudo(date_sta,-3)
    print(date2)

    i = row_sta
    count = 0
    while ws.cells(i,col_taisho).value != 'END' :  
        
        # ３行ごとに値を入手する
        if count % 3 == 0:
            taisho = ws.cells(i,col_taisho).value  
            kenmei = ws.cells(i,col_kenmei).value  
            kubun = ws.cells(i,col_kubun).value  
            date1 = ws.cells(i,col_date1).value  
            date2 = ws.cells(i,col_date2).value  
            date3 = ws.cells(i,col_date3).value  
            date4 = ws.cells(i,col_date4).value  

            try:
                tmp = kubun + 1
                flg_mensu = 1
            except:
                flg_mensu = 0

            if flg_mensu == 1:
                value1 = 1
                value2 = 0.5
                value3 = 0.1
            else:
                value1 = 0.5
                value2 = 0.1
                value3 = 0.1

        bumon = ws.cells(i,col_bumon).value

        #print( i , count%3, taisho,kenmei,kubun,date1,date2,date3,date4)

        #処理対象フラグが無い場合は次の行へ。
        if taisho == None:
            count+=1
            i+=1
            continue

        #該当行を一旦クリア
        ws.Range(  ws.cells(i,col_cal) , ws.cells(i,col_end) ).ClearContents()

        if bumon =='部門1' :
        
            sabun1 = date1 - date_sta
            sabun2 = date2 - date_sta

            for j in range(sabun1.days,sabun2.days ):
                ws.cells(i,col_cal + j).value= value1

            date_syuryo = jitudo(date2,5)
            sabun2a = date_syuryo - date_sta

            for j in range(sabun2.days , sabun2a.days ):
                ws.cells(i,col_cal + j).value= value2

            sabun3 = date3 - date_sta
            for j in range(sabun2a.days , sabun3.days ):
                ws.cells(i,col_cal + j).value= value3
        
        elif bumon =='部門2' :

            sabun2 = date2 - date_sta
            sabun2a = date_syuryo - date_sta

            for j in range(sabun2.days,sabun2a.days ):
                ws.cells(i,col_cal + j).value=1

        elif bumon =='部門3' and flg_mensu == 1:

            sabun4 = date4 - date_sta

            for j in range(sabun3.days,sabun4.days ):
                ws.cells(i,col_cal + j).value=1

        elif bumon =='部門3' and flg_mensu == 0:

            for j in range(sabun2.days,sabun3.days ):
                ws.cells(i,col_cal + j).value=1



        count+=1
        i+=1


    wb.Save()

