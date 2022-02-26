'https://www.mutable.work/entry/upload-to-sharepoint-by-vba

Sub SaveAtSharepoint()

    Dim url As String '保存先のシェアポイントのURL
    Dim conv_url As String 'シェアポイントのURLをフォルダ名に変換した文字列。フルパスなのでファイル名まで。
    Dim local_full_path As String 'シェアポイントに保存したいデータのフルパス
    Dim fso As Object 'FileSystemObjectのインスタンス化
    
    '>初期設定
    url = "シェアポイント上のURL" & "ファイル名.xlsx"
    local_full_path = "アップロードしたいファイルのフルパス"
    '<初期設定
    
    Set fso = CreateObject("Scripting.FileSystemObject")  'インスタンス生成
    conv_url = ConvertDirectoryPath(url)
    
    If fso.FileExists(local_full_path) Then
        fso.CopyFile local_full_path, conv_url
    End If
    
    Set fso = Nothing

End Sub

Function ConvertDirectoryPath(path) As String
    'このプロシジャはシェアポイントのURLをドキュメントライブラリのディレクトリパスに変換する
    ConvertDirectoryPath = Replace(path, " ", "%20")
    ConvertDirectoryPath = Replace(ConvertDirectoryPath, "/", "\")
    ConvertDirectoryPath = Replace(ConvertDirectoryPath, "http:", "")
End Function