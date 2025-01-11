import win32com.client
import polars as pl



# Excelへのカラム出力
def excel_out_col(filename, sheetname, _tuple, startRow, startCol):
   
    excel = win32com.client.GetObject(Class="Excel.Application")  # 開いているExcelアプリケーションへの参照を取得
    for wb in excel.Workbooks:   # 開いているワークブックの中から対象ブックを探す
        if wb.Name == filename:
            target_wb = wb
            break

    ws = target_wb.Worksheets(sheetname)                     #シートを取得
    ws.Range(ws.Cells(startRow,startCol),ws.Cells(startRow, startCol+len(_tuple)-1)).ClearContents()  #シートをクリア （１行目のカラムの部分）
    ws.Range(ws.Cells(startRow,startCol),ws.Cells(startRow, startCol+len(_tuple)-1)).Value = _tuple   #tuple-Excel出力  

# Excelへのデータ出力
def excel_out_data(filename, sheetname, _tuple, startRow, startCol):

    excel = win32com.client.GetObject(Class="Excel.Application") # 開いているExcelアプリケーションへの参照を取得
    for wb in excel.Workbooks:  # 開いているワークブックの中から対象ブックを探す
        if wb.Name == filename:
            target_wb = wb
            break

    ws = target_wb.Worksheets(sheetname)                          #シートを取得
    ws.Range(ws.Cells(2,1),ws.Cells(10000,100)).ClearContents()  #シートをクリア
    ws.Range(ws.Cells(startRow,startCol),ws.Cells(startRow+len(_tuple)-1, startCol+len(_tuple[0])-1)).Value = _tuple #tuple-Excel出力  len(_tuple[0])は列数を表す
    ws.Activate()                                                                                     #対象シートをアクティベート
    target_wb.Save()         

if __name__ == '__main__':

    df = pl.read_excel('質問事項.xlsx',sheet_name='チェック事項')
    filename ='質問事項.xlsx'
    sheetname ='Sheet4' 
    tuple=('番号','チェック事項')
    excel_out_col(filename=filename, sheetname=sheetname, _tuple=tuple, startRow=1, startCol=1)  
    excel_out_data(filename=filename, sheetname=sheetname, _tuple=df.rows(), startRow=2, startCol=1)    # df.rows() はタプル変換 
    



