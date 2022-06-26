Imports Microsoft.Office.Interop

Public Class Form1

    Private prioKoteiData As Object   '工程ごとの稼働日などの情報

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click

        Dim day1 As Date
        Dim bFlg As Boolean

        bFlg = setKoteiData()  '工程ごとの稼働日などの情報を prioKoteiData へ取り込む

        If bFlg Then
            day1 = KoteiWorkday(#2022/06/10#, -5, "M020")
        End If

        Debug.Print(day1)

    End Sub

    Private Function setKoteiData() As Boolean

        Dim ap As New Excel.Application
        Dim wb As Excel.Workbook
        Dim sh As Excel.Worksheet
        Dim nEndRow, nEndCol As Integer

        'ファイルオープン
        Try
            wb = ap.Workbooks.Open("C:\Users\arwml\source\repos\日程再展開\工程マスタ.xlsx")
        Catch ex As Exception
            Call System.Runtime.InteropServices.Marshal.ReleaseComObject(ap)
            Return False
        End Try

        'シートオープン
        Try
            sh = wb.Worksheets("2_工程情報")
        Catch ex As Exception
            Call System.Runtime.InteropServices.Marshal.ReleaseComObject(ap)
            Call System.Runtime.InteropServices.Marshal.ReleaseComObject(wb)
            Return False
        End Try

        '工程情報シートの最終行取得
        nEndRow = sh.Cells(sh.Rows.Count, 1).end(Excel.XlDirection.xlUp).row  'シートの最終行を取得 

        '工程情報シートの最終列取得
        nEndCol = sh.Cells(1, sh.Columns.Count).end(Excel.XlDirection.xlToLeft).column  'シートの最終列を取得 

        '工程情報シートをdataに取り込む  '工程情報シートは、１列目に工程コード、７列目から稼働日=1が記載されている前提。
        prioKoteiData = sh.Range(sh.Cells(1, 1), sh.Cells(nEndRow, nEndCol)).Value

        ap.Quit()
        Call System.Runtime.InteropServices.Marshal.ReleaseComObject(ap)
        Call System.Runtime.InteropServices.Marshal.ReleaseComObject(wb)
        Call System.Runtime.InteropServices.Marshal.ReleaseComObject(sh)

        Return True

    End Function


    Private Function KoteiWorkday(ByVal BaseDate As Date, ByVal nOffsetDays As Integer, ByVal KoteiCd As String) As Date

        Dim i, j As Integer

        'オフセット日数がゼロの場合、基準日をそのまま返す。
        If nOffsetDays = 0 Then
            Return BaseDate
        End If

        KoteiWorkday = #1999/12/31#

        Try
            'data上のKoteiCdの行を探索
            Dim nRow As Integer
            For i = 1 To UBound(prioKoteiData, 1)
                If KoteiCd = prioKoteiData(i, 1) Then
                    nRow = i
                    Exit For
                End If
            Next

            'data上のBaseDateの列を探索
            Dim nColBaseDate As Integer
            For j = 7 To UBound(prioKoteiData, 2)
                If BaseDate = prioKoteiData(1, j) Then
                    nColBaseDate = j
                End If
            Next

            'オフセット日の計算
            If nOffsetDays > 0 Then '未来へのオフセットの場合
                j = 0
                Do While nOffsetDays > 0   'オフセット残がなくなるまでループ
                    j += 1
                    If prioKoteiData(nRow, nColBaseDate + j) = 1 Then  '基準＋j日目が 1 実働日の場合
                        nOffsetDays -= 1
                    End If
                Loop
                KoteiWorkday = prioKoteiData(1, nColBaseDate + j)  '戻り値にオフセット日をセットする  

            Else '過去へのオフセットの場合
                j = 0
                Do While nOffsetDays < 0   'オフセット残がなくなるまでループ
                    j += 1
                    If prioKoteiData(nRow, nColBaseDate - j) = 1 Then  '基準＋j日目が 1 実働日の場合
                        nOffsetDays += 1
                    End If
                Loop
                KoteiWorkday = prioKoteiData(1, nColBaseDate - j)  '戻り値にオフセット日をセットする  
            End If

        Catch ex As Exception
            Return #1999/12/31#

        End Try


    End Function

End Class
