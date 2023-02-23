Sub kyujitsu()

Dim i, j As Integer
Dim wd As Integer

    With ActiveSheet
    
        
        .Cells(1, 5) = Date
        For j = 6 To 365
            .Cells(1, j).Value = .Cells(1, j - 1).Value + 1
        Next
        
        
        j = 1
        Do While j < 365
        
            wd = Weekday(.Cells(1, j).Value)
            Debug.Print (j & wd)
        
            If wd = 1 Or wd = 7 Then
                
                i = 1
                Do While i < 10
                    .Cells(i, j).Interior.ColorIndex = 15
                    i = i + 1
                Loop

            Else
                .Cells(1, j).Interior.ColorIndex = 0
            End If
            
            j = j + 1
        Loop
    
    End With


End Sub