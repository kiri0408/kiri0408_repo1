Attribute VB_Name = "Module1"
Option Explicit

Public data1 As Variant
Public message1 As String

Function check_date1(ByVal kubun As String, ByVal col_name As String, ByVal col_ord As Integer, ByVal col_kubun As Integer, ByVal col_date As Integer, ByVal row_sta As Integer, ByVal row_end As Integer) As String

    Dim i As Integer
    Dim ord4_new, ord4_old As String
    Dim date_new, date_old As Variant
    
    ord4_new = ""
    date_new = ""
    i = row_sta
    While i <= row_end
    
        '対象の区分の日付とオーダ４桁を取得（計画or見込）
        If data1(i, col_kubun) = kubun Then
            date_old = date_new
            ord4_old = ord4_new
            date_new = data1(i, col_date)
            ord4_new = Left(data1(i, col_ord), 4)
        
            'オーダ４桁が同じでかつ日付が異なる場合にワーニングとして記録する。
            If ord4_new = ord4_old And date_new <> date_old And date_old <> "" Then
                message1 = message1 & Str(i) & "行目 " & ord4_new & " " & col_name & " " & kubun & " " & CStr(date_new) & vbCrLf
            End If
        
        End If
        
        i = i + 1
    Wend
    
    check_date1 = message1
End Function



Function check_date_main(ByVal filepath As String, ByVal sheetname As String) As Boolean
    Dim wb2 As Workbook
    Dim ws2 As Worksheet
    Dim dataRange As Range
    Dim i As Integer
    
    ' 他のワークブックを開く
    Set wb2 = Workbooks.Open(filepath)
    
    ' シートを参照
    Set ws2 = wb2.Sheets(sheetname)
    
    ' チェック対象のワークブックの範囲を指定
    Set dataRange = ws2.Range("A1:CZ1000")
    
    ' 範囲を配列に取り込む
    data1 = dataRange.Value
    
    'オーダの列は３行ごとにオーダが記載されているので埋める
    Dim col_ord As Integer
    col_ord = 6
    For i = 1 To 1000
        If data1(i, col_ord) = "" Then
            data1(i, col_ord) = data1(i - 1, col_ord)
        End If
    Next i
           
    ' オーダ４桁内の日付整合チェック
    message1 = "オーダ４桁内で日付が不整合です" & vbCrLf
    message1 = check_date1("計画", "DR1", 6, 7, 8, 2, 1000) '数字は、オーダ列、区分列、チェック対象日付列,開始行、終了行
    message1 = check_date1("見込", "DR1", 6, 7, 8, 2, 1000)
    message1 = check_date1("計画", "客先", 6, 7, 10, 2, 1000)
    message1 = check_date1("見込", "客先", 6, 7, 10, 2, 1000)
    
    '日付不整合があった場合にメッセージを表示する。
    If Len(message1) > 20 Then   '日付不整合があればメッセージが２０文字より大きい
        MsgBox (message1)
    End If

    

End Function


Sub jikko()

    Dim a As Boolean
    
    a = check_date_main("C:\Users\arwml\Documents\shareiyaguti.xlsx", "Sheet1")
     
End Sub


