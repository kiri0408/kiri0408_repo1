Attribute VB_Name = "Module1"
Sub row_insert()
    ActiveSheet.Rows(10000).Copy
    ActiveSheet.Rows(ActiveCell.Row + 1).Insert Shift:=xlDown
End Sub


