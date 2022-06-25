Imports Microsoft.Office.Interop



'新規作成の処理前の データ終了行 Me.txtTargetFin.Text 
'設定ファイル パス        Me.txtSettingFile.Text
'小日程シートファイルパス Me.txtNitteiFile.Text 
'小日程シートシート名     Me.txtNitteiSheet.Text
'Private Function setAtoKoteiMaeKotei(）
'  設定ファイルパスがなかった場合はパス
'「工程」シートがなかった場合は、パス。


Public Class Form1
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        Dim ap As New Excel.Application
        Dim wb As Excel.Workbook
        Dim sh As Excel.Worksheet
        Dim sh_kotei As Excel.Worksheet
        Dim key, key_next As String
        Dim kotei, kotei_next As String
        Dim i, j As Integer

        wb = ap.Workbooks.Open("C:\Users\arwml\source\repos\関連keycode追加\Book1a.xlsx")
        sh = wb.Worksheets("Sheet1")





        Try
            sh_kotei = wb.Worksheets("工程")
        Catch ex As Exception
            Call System.Runtime.InteropServices.Marshal.ReleaseComObject(ap)
            Call System.Runtime.InteropServices.Marshal.ReleaseComObject(wb)
            Call System.Runtime.InteropServices.Marshal.ReleaseComObject(sh)
            Exit Sub
        End Try





        Try
            ap.Visible = False

            'Dim data(10000, 2) As Object
            'Dim data_ato(100, 100) As Object  '後工程シートのデータ
            'Dim data_mae(100, 100) As Object  '前工程シートのデータ
            Dim sta_row, end_row As Integer  '小日程シートの開始行、終了行
            Dim kotei_i, kotei_j, row_jikoutei As Integer  '前工程 後工程が記載されたシートのセル位置用
            Dim xlRange_fr As Excel.Range    '前工程 後工程が記載されたシートからのセルコピー用
            Dim xlRange_to As Excel.Range    '前工程 後工程が記載されたシートからのセルコピー用


            'data = sh.Range(sh.Cells(1, 1), sh.Cells(10000, 2)).Value     'excel ->  配列へ取り込み
            'data_ato = sh_kotei.Range(sh_kotei.Cells(1, 1), sh_kotei.Cells(100, 100)).Value     'excel ->  配列へ取り込み
            'data_mae = sh_mae.Range(sh_mae.Cells(1, 1), sh_mae.Cells(100, 100)).Value     'excel ->  配列へ取り込み

            'key = data_ato(1, 1)
            'kotei = data_ato(1, 2)
            'key_next = data_ato(2, 1)
            'kotei_next = data_ato(2, 2)

            sta_row = 2


            row_jikoutei = 10 '後工程情報は１０行目以降
            kotei_j = 4       '後工程情報は４列目以降
            Do While sh_kotei.Cells(row_jikoutei, kotei_j).value <> ""  '工程シートの設定値でループ   '後工程情報は１０行目
                '工程シートから 設定値を取得する
                key = sh_kotei.Cells(row_jikoutei, kotei_j).value                'row_jikoutei：自工程    kotei_j：計画種別 
                kotei = sh_kotei.Cells(row_jikoutei, kotei_j + 1).value          'row_jikoutei：自工程    kotei_j:工程コード 
                key_next = sh_kotei.Cells(row_jikoutei + 1, kotei_j).value       'row_jikoutei+1行目：後工程の先頭    kotei_j：計画種別 
                kotei_next = sh_kotei.Cells(row_jikoutei + 1, kotei_j + 1).value 'row_jikoutei+1行目：後工程の先頭    kotei_j:工程コード

                end_row = sh.Cells(sh.Rows.Count, 1).end(Excel.XlDirection.xlUp).row  '小日程シートの最終行を取得 
                i = sta_row
                Do While i <= end_row   '小日程シートを探索
                    '後工程シートの該当キーコードに一致したが、下の行に後工程キーコードが未設定の場合 
                    If Strings.Right(sh.Cells(i, 1).value, 2) + sh.Cells(i, 2).value = key + kotei And Strings.Right(sh.Cells(i + 1, 1).value, 2) + sh.Cells(i + 1, 2).value <> key_next + kotei_next Then
                        '後工程シートに記載された後工程を行挿入する
                        kotei_i = row_jikoutei + 1
                        Do While sh_kotei.Cells(kotei_i, kotei_j).value <> ""
                            i = i + 1  '該当行の下に行挿入するため iを1増やす 
                            sh.Range(i.ToString() + ":" + i.ToString()).Insert()  '行挿入
                            end_row = end_row + 1

                            xlRange_fr = sh_kotei.Cells.Range(sh_kotei.Cells(kotei_i, kotei_j), sh_kotei.Cells(kotei_i, kotei_j + 1))  '後工程シートのコピー元セルをセット
                            xlRange_to = sh.Cells.Range(sh.Cells(i, 1), sh.Cells(i, 2))                                          'コピー先セルをセット
                            xlRange_fr.Copy(xlRange_to)                                                                          'セルコピー実行

                            sh.Cells(i, 1).value = Strings.Left(sh.Cells(i - 1, 1).value, 8) + sh.Cells(i, 1).value              'コピーしたセルに 上の行のオーダ８桁を付与しkeycodeとする。 

                            kotei_i += 1
                        Loop
                    End If
                    i = i + 1
                Loop
                kotei_j += 3  '３列間隔で後工程情報をセットしている
            Loop

            row_jikoutei = 7  '前工程情報は７行目
            kotei_j = 4       '前工程情報は４列目以降
            Do While sh_kotei.Cells(row_jikoutei, kotei_j).value <> ""  '工程シートの設定値でループ   '前工程情報は７行目
                '工程シートから 設定値を取得する
                key = sh_kotei.Cells(row_jikoutei, kotei_j).value                'row_jikoutei：自工程    kotei_j：計画種別 
                kotei = sh_kotei.Cells(row_jikoutei, kotei_j + 1).value          'row_jikoutei：自工程    kotei_j:工程コード 
                key_next = sh_kotei.Cells(row_jikoutei - 1, kotei_j).value       'row_jikoutei-1行目：前工程の先頭    kotei_j：計画種別 
                kotei_next = sh_kotei.Cells(row_jikoutei - 1, kotei_j + 1).value 'row_jikoutei-1行目：前工程の先頭    kotei_j:工程コード

                end_row = sh.Cells(sh.Rows.Count, 1).end(Excel.XlDirection.xlUp).row  '小日程シートの最終行を取得 
                i = sta_row
                Do While i <= end_row   '小日程シートを探索
                    '工程シートの該当キーコードに一致したが、上の行に前工程キーコードが未設定の場合 
                    If Strings.Right(sh.Cells(i, 1).value, 2) + sh.Cells(i, 2).value = key + kotei And Strings.Right(sh.Cells(i - 1, 1).value, 2) + sh.Cells(i - 1, 2).value <> key_next + kotei_next Then
                        '工程シートに記載された工程を行挿入する
                        kotei_i = row_jikoutei - 1
                        Do While sh_kotei.Cells(kotei_i, kotei_j).value <> ""
                            'i = i + 1  '前工程の場合は上に行挿入するためこの行は不要 
                            sh.Range(i.ToString() + ":" + i.ToString()).Insert()  '行挿入
                            end_row = end_row + 1

                            xlRange_fr = sh_kotei.Cells.Range(sh_kotei.Cells(kotei_i, kotei_j), sh_kotei.Cells(kotei_i, kotei_j + 1))  '後工程シートのコピー元セルをセット
                            xlRange_to = sh.Cells.Range(sh.Cells(i, 1), sh.Cells(i, 2))                                          'コピー先セルをセット
                            xlRange_fr.Copy(xlRange_to)                                                                          'セルコピー実行

                            sh.Cells(i, 1).value = Strings.Left(sh.Cells(i + 1, 1).value, 8) + sh.Cells(i, 1).value              'コピーしたセルに 下の行のオーダ８桁を付与しkeycodeとする。 

                            kotei_i -= 1  '前工程情報は 工程シートの行を上方向に順番に探索するので -1
                        Loop
                    End If
                    i = i + 1
                Loop
                kotei_j += 3  '３列間隔で後工程情報をセットしている
            Loop


            'data(2, 2) = "test1"                                          '配列の加工
            'sh.Range(sh.Cells(1, 1), sh.Cells(10000, 2)).Value = data     '配列 -> excel へ戻し

            wb.SaveAs("C:\Users\arwml\source\repos\関連keycode追加\output1.xlsx")


        Catch ex As Exception
            Throw
        Finally
            ap.Quit()
            Call System.Runtime.InteropServices.Marshal.ReleaseComObject(ap)
            Call System.Runtime.InteropServices.Marshal.ReleaseComObject(wb)
            Call System.Runtime.InteropServices.Marshal.ReleaseComObject(sh)
            Call System.Runtime.InteropServices.Marshal.ReleaseComObject(sh_kotei)

            MessageBox.Show("処理完了")
        End Try
    End Sub
End Class

  
  
  