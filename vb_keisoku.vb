Public Class Form1
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click

        Dim xl As Object 'Excel.Application
        Dim wb As Object 'Excel.Workbook
        Dim ws As Object 'Excel.Worksheet

        xl = CreateObject("Excel.Application")
        wb = xl.Workbooks.Open("C:\vb\test1\test_excel\list_mid.xlsx")
        'wb = xl.Workbooks.Open("list_min.xlsx")
        xl.Visible = False

        ws = wb.Worksheets("Sheet1")

        MsgBox(ws.cells(2, 2).value)

        '処理開始時刻を記憶
        Dim start As DateTime = Now

        Dim i, j As Integer
        Dim sum As Long

        sum = 0

        With ws

            i = 1
            Do While i < 500

                j = 1
                Do While j < 20

                    sum = .cells(i, j).value

                    'Debug.Print(i & "   " & sum)


                    j = j + 1
                Loop

                i = i + 1
            Loop

        End With

        '処理時間を計算（現在時刻－処理開始時刻）
        Dim span As TimeSpan = Now - start

        MessageBox.Show(String.Format("処理時間は{0}秒です。", span.TotalSeconds))

        MsgBox(sum)

        xl = Nothing
        wb = Nothing
        ws = Nothing


    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        Dim xl As Object 'Excel.Application
        Dim wb As Object 'Excel.Workbook
        Dim ws As Object 'Excel.Worksheet

        xl = CreateObject("Excel.Application")
        wb = xl.Workbooks.Open("C:\vb\test1\test_excel\list_mid.xlsx")
        'wb = xl.Workbooks.Open("list_min.xlsx")
        xl.Visible = False

        ws = wb.Worksheets("Sheet1")

        MsgBox(ws.cells(2, 2).value)

        '処理開始時刻を記憶
        Dim start As DateTime = Now

        Dim i, j As Integer
        Dim sum As Long

        Dim data1 As Object

        sum = 0

        With ws


            data1 = .range(.cells(1, 1), .cells(500, 20))

            i = 1
            Do While i < 500

                j = 1
                Do While j < 20

                    sum = data1(i, j).value

                    'Debug.Print(i & "   " & sum)


                    j = j + 1
                Loop

                i = i + 1
            Loop

        End With

        '処理時間を計算（現在時刻－処理開始時刻）
        Dim span As TimeSpan = Now - start

        MessageBox.Show(String.Format("処理時間は{0}秒です。", span.TotalSeconds))

        MsgBox(sum)

        xl = Nothing
        wb = Nothing
        ws = Nothing

    End Sub
End Class
