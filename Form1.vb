
'Imports System
'Imports System.IO
'Imports System.Text
'Imports System.Data.OleDb
'Imports Microsoft.Office.Interop
Imports Microsoft.VisualBasic.FileIO


Public Class Form1


    Private Shared ini_file As String = ""


    '起動時
    Private Sub Form1_Load(ByVal sender As Object,
                           ByVal e As System.EventArgs) Handles Me.Load


        MessageBox.Show(System.Environment.UserName)
        MessageBox.Show(System.Environment.MachineName)
        Dim dt1 As DateTime = DateTime.Now
        MsgBox(dt1.ToString("yyyyMMdd_HHmmss"))

        ' カレントディレクトリを取得する
        Dim stCurrentDir As String = System.IO.Directory.GetCurrentDirectory()
        Dim hantei As Integer


        ' カレントディレクトリのiniファイルを検索する
        hantei = 0
        For Each filename As String In System.IO.Directory.GetFiles(stCurrentDir, "ini*.csv")
            hantei = 1
            ini_file = filename
            Exit For
        Next

        'iniファイルが無い場合は終了
        If hantei = 0 Then
            MsgBox("iniファイルがみつかりません")
            Me.Close()
        End If


        Try
            Using parser As New TextFieldParser(ini_file, System.Text.Encoding.GetEncoding("Shift_JIS"))

                parser.TextFieldType = FieldType.Delimited
                parser.SetDelimiters(",")

                Dim i As Integer

                i = 1
                While Not parser.EndOfData
                    Dim row As String() = parser.ReadFields()

                    If i = 2 Then
                        TextBox1.Text = row(1)
                    End If

                    i = i + 1
                End While
            End Using

        Catch ex As System.Exception
            MsgBox("エラー" & vbCrLf & ex.Message)
            Me.Close()

        End Try



    End Sub


    '検索ボタン
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click

        '変数宣言
        Dim excel As New Microsoft.Office.Interop.Excel.Application
        Dim sh As Microsoft.Office.Interop.Excel.Worksheet
        Dim wb As Microsoft.Office.Interop.Excel.Workbook


        Dim input1 As String
        'Dim ex As Exception


        input1 = TextBox1.Text

        'MessageBox.Show(input1)


        ' カレントディレクトリを取得する
        'Dim stCurrentDir As String = System.IO.Directory.GetCurrentDirectory()

        'ファイルオープン
        Try
            wb = excel.Workbooks.Open(input1)
            sh = wb.Sheets(“Sheet1”)
        Catch ex As System.Exception
            MsgBox("エラー" & vbCrLf & ex.Message)
            Me.Close()

        End Try



        With sh
            Dim data1 As Object

            data1 = .Range(.Cells(1, 1), .Cells(3, 3)).Value

            data1(3, 3) = 999

            .Range(.Cells(1, 1), .Cells(3, 3)).Value = data1

        End With

        'MsgBox(sh.Range(“A2”).Value)

        wb.Save()

        excel.Quit()

        MsgBox("ファイルを保存しました")


    End Sub

    '終了ボタンクリック
    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click



        'CSVファイルのエンコードを指定（今回はShift_JIS）
        Dim enc As System.Text.Encoding = System.Text.Encoding.GetEncoding("Shift_JIS")

        ' カレントディレクトリを取得する
        'Dim stCurrentDir As String = System.IO.Directory.GetCurrentDirectory()

        '書き込むファイルを開く
        'Dim sr As New System.IO.StreamWriter(stCurrentDir & "\ini.csv", False, enc)
        Dim sr As New System.IO.StreamWriter(ini_file, False, enc)

        '１行目  ヘッダ
        sr.Write("項目")
        sr.Write(","c)
        sr.Write("値")
        sr.Write(vbCrLf)

        '2行目
        sr.Write("対象ファイル")
        sr.Write(","c)
        sr.Write(TextBox1.Text)
        sr.Write(vbCrLf)

        '閉じる（解放）
        sr.Close()




        Me.Close()
    End Sub

    'ファイル選択ボタンクリック
    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click

        Dim ofd As New OpenFileDialog()

        ofd.Filter = "すべてのファイル(*.*)|*.*|Excelファイル|*.xlsx;*.xlsm"
        ofd.FilterIndex = 2  '2番目が選択されているようにする
        ofd.Title = "開くファイルを選択してください"
        ofd.RestoreDirectory = True   'ダイアログボックスを閉じる前に現在のディレクトリを復元するようにする

        'ダイアログを表示する
        If ofd.ShowDialog() = DialogResult.OK Then
            'Console.WriteLine(ofd.FileName)
            TextBox1.Text = ofd.FileName
        End If


    End Sub

End Class