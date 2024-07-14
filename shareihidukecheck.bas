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
    
        '�Ώۂ̋敪�̓��t�ƃI�[�_�S�����擾�i�v��or�����j
        If data1(i, col_kubun) = kubun Then
            date_old = date_new
            ord4_old = ord4_new
            date_new = data1(i, col_date)
            ord4_new = Left(data1(i, col_ord), 4)
        
            '�I�[�_�S���������ł����t���قȂ�ꍇ�Ƀ��[�j���O�Ƃ��ċL�^����B
            If ord4_new = ord4_old And date_new <> date_old And date_old <> "" Then
                message1 = message1 & Str(i) & "�s�� " & ord4_new & " " & col_name & " " & kubun & " " & CStr(date_new) & vbCrLf
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
    
    ' ���̃��[�N�u�b�N���J��
    Set wb2 = Workbooks.Open(filepath)
    
    ' �V�[�g���Q��
    Set ws2 = wb2.Sheets(sheetname)
    
    ' �`�F�b�N�Ώۂ̃��[�N�u�b�N�͈̔͂��w��
    Set dataRange = ws2.Range("A1:CZ1000")
    
    ' �͈͂�z��Ɏ�荞��
    data1 = dataRange.Value
    
    '�I�[�_�̗�͂R�s���ƂɃI�[�_���L�ڂ���Ă���̂Ŗ��߂�
    Dim col_ord As Integer
    col_ord = 6
    For i = 1 To 1000
        If data1(i, col_ord) = "" Then
            data1(i, col_ord) = data1(i - 1, col_ord)
        End If
    Next i
           
    ' �I�[�_�S�����̓��t�����`�F�b�N
    message1 = "�I�[�_�S�����œ��t���s�����ł�" & vbCrLf
    message1 = check_date1("�v��", "DR1", 6, 7, 8, 2, 1000) '�����́A�I�[�_��A�敪��A�`�F�b�N�Ώۓ��t��,�J�n�s�A�I���s
    message1 = check_date1("����", "DR1", 6, 7, 8, 2, 1000)
    message1 = check_date1("�v��", "�q��", 6, 7, 10, 2, 1000)
    message1 = check_date1("����", "�q��", 6, 7, 10, 2, 1000)
    
    '���t�s�������������ꍇ�Ƀ��b�Z�[�W��\������B
    If Len(message1) > 20 Then   '���t�s����������΃��b�Z�[�W���Q�O�������傫��
        MsgBox (message1)
    End If

    

End Function


Sub jikko()

    Dim a As Boolean
    
    a = check_date_main("C:\Users\arwml\Documents\shareiyaguti.xlsx", "Sheet1")
     
End Sub


