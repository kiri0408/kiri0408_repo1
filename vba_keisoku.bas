Attribute VB_Name = "Module1"



Sub ReferOtherBook()
    Dim ex      As New Excel.Application    '// 処理用Excel
    Dim wb      As Workbook                 '// ワークブック
    Dim sPath                               '// ブックファイルパス
    Dim r       As Range                    '// 取得対象のセル範囲
    Dim sht     As Worksheet                '// 参照シート
    
    '// 開くブックを指定
    sPath = "C:\vb\test1\test_excel\list_mid.xlsx"
    
    '// 読み取り専用で開く
    Set wb = ex.Workbooks.Open(Filename:=sPath, UpdateLinks:=0, ReadOnly:=True, IgnoreReadOnlyRecommended:=True)
    
    '// 一番左のシートの入力セル範囲を取得
    Set r = wb.Worksheets(1).UsedRange
    
    '// 各シートのA1セルを取得
    For Each sht In wb.Worksheets
        Set r = sht.Range("A1")
        
        Debug.Print r.Value
    Next
    
    Dim i, j As Integer
    Dim sum As Long
      Dim startTime As Double
  Dim endTime As Double
  Dim processTime As Double
  
    startTime = Timer
    
    With wb.Worksheets("Sheet1")
    
        i = 1
        Do While i < 500
        
            j = 1
            Do While j < 20
            
                sum = sum + .Cells(i, j)
            
                'Debug.Print (i & "   " & sum)
                
            
                j = j + 1
            Loop
        
            i = i + 1
        Loop
    
    End With
    
    Debug.Print ("合計 : " & sum)
    
      '終了時間取得
  endTime = Timer
 
  '処理時間表示
  processTime = endTime - startTime
  Debug.Print ("処理時間：" & processTime)
  
    
    '// ブックを閉じる
    Call wb.Close
    
    '// Excelアプリケーションを閉じる
    Call ex.Application.Quit
End Sub



Sub ReferOtherBook2()
    Dim ex      As New Excel.Application    '// 処理用Excel
    Dim wb      As Workbook                 '// ワークブック
    Dim sPath                               '// ブックファイルパス
    Dim r       As Range                    '// 取得対象のセル範囲
    Dim sht     As Worksheet                '// 参照シート
    
    '// 開くブックを指定
    sPath = "C:\vb\test1\test_excel\list_mid.xlsx"
    
    '// 読み取り専用で開く
    Set wb = ex.Workbooks.Open(Filename:=sPath, UpdateLinks:=0, ReadOnly:=True, IgnoreReadOnlyRecommended:=True)
    
    '// 一番左のシートの入力セル範囲を取得
    Set r = wb.Worksheets(1).UsedRange
    
    '// 各シートのA1セルを取得
    For Each sht In wb.Worksheets
        Set r = sht.Range("A1")
        
        Debug.Print r.Value
    Next
    
    Dim i, j, k As Integer
    Dim sum As Long
      Dim startTime As Double
  Dim endTime As Double
  Dim processTime As Double
  
  
  Dim data1 As Variant
  
  
    startTime = Timer
    
    With wb.Worksheets("Sheet1")
    
        data1 = .Range(.Cells(1, 1), .Cells(500, 20))
    
'        k = 1
'        Do While k <= 10
    
            i = 1
            Do While i < 500
            
                j = 1
                Do While j < 20
                
                    sum = sum + data1(i, j)
                
                    'Debug.Print (i & "   " & sum)
                    
                
                    j = j + 1
                Loop
            
                i = i + 1
            Loop
        
'            k = k + 1
'        Loop
    
    End With
    
    Debug.Print ("合計 : " & sum)
    
      '終了時間取得
  endTime = Timer
 
  '処理時間表示
  processTime = endTime - startTime
  Debug.Print ("処理時間：" & processTime)
  
    
    '// ブックを閉じる
    Call wb.Close
    
    '// Excelアプリケーションを閉じる
    Call ex.Application.Quit
End Sub

