Option Explicit


Private Sub Auto_Open()
 
    Dim i, flg As Integer
    Dim data As Variant
    
    
    With ThisWorkbook.Worksheets("予定")
    
        'ソート
        .Range(.Cells(2, 1), .Cells(1000, 5)).Sort Key1:=Range("A1") _
        , Order1:=xlAscending _
        , Header:=xlGuess _
        , MatchCase:=False _
        , Orientation:=xlTopToBottom _
        , SortMethod:=xlPinYin
        
        '書式クリア
        '.Range(.Cells(1, 1), .Cells(1000, 5)).ClearFormats
        .Range(.Cells(1, 1), .Cells(1000, 5)).Interior.ColorIndex = 0
        
        
        data = .Range(.Cells(1, 1), .Cells(1000, 5))
        
        flg = 0
        i = 2
        Do While data(i, 1) <> ""
        
            If data(i, 1) < Date Then
                .Cells(i, 1).Interior.ColorIndex = 3  '3赤色
                flg = i
            ElseIf data(i, 1) = Date Then
                .Cells(i, 1).Interior.ColorIndex = 6  '6黄色
                flg = i
            ElseIf data(i, 1) < Date + 3 Then
                .Cells(i, 1).Interior.ColorIndex = 4  '4緑
                flg = i
            End If
        
            i = i + 1
        Loop
        
        '該当があればシートをアクティブ
        If flg > 0 Then
            .Activate
            .Cells(flg, 1).Select
        End If
    
    End With
    
End Sub
