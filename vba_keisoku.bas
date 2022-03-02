Attribute VB_Name = "Module1"



Sub ReferOtherBook()
    Dim ex      As New Excel.Application    '// �����pExcel
    Dim wb      As Workbook                 '// ���[�N�u�b�N
    Dim sPath                               '// �u�b�N�t�@�C���p�X
    Dim r       As Range                    '// �擾�Ώۂ̃Z���͈�
    Dim sht     As Worksheet                '// �Q�ƃV�[�g
    
    '// �J���u�b�N���w��
    sPath = "C:\vb\test1\test_excel\list_mid.xlsx"
    
    '// �ǂݎ���p�ŊJ��
    Set wb = ex.Workbooks.Open(Filename:=sPath, UpdateLinks:=0, ReadOnly:=True, IgnoreReadOnlyRecommended:=True)
    
    '// ��ԍ��̃V�[�g�̓��̓Z���͈͂��擾
    Set r = wb.Worksheets(1).UsedRange
    
    '// �e�V�[�g��A1�Z�����擾
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
    
    Debug.Print ("���v : " & sum)
    
      '�I�����Ԏ擾
  endTime = Timer
 
  '�������ԕ\��
  processTime = endTime - startTime
  Debug.Print ("�������ԁF" & processTime)
  
    
    '// �u�b�N�����
    Call wb.Close
    
    '// Excel�A�v���P�[�V���������
    Call ex.Application.Quit
End Sub



Sub ReferOtherBook2()
    Dim ex      As New Excel.Application    '// �����pExcel
    Dim wb      As Workbook                 '// ���[�N�u�b�N
    Dim sPath                               '// �u�b�N�t�@�C���p�X
    Dim r       As Range                    '// �擾�Ώۂ̃Z���͈�
    Dim sht     As Worksheet                '// �Q�ƃV�[�g
    
    '// �J���u�b�N���w��
    sPath = "C:\vb\test1\test_excel\list_mid.xlsx"
    
    '// �ǂݎ���p�ŊJ��
    Set wb = ex.Workbooks.Open(Filename:=sPath, UpdateLinks:=0, ReadOnly:=True, IgnoreReadOnlyRecommended:=True)
    
    '// ��ԍ��̃V�[�g�̓��̓Z���͈͂��擾
    Set r = wb.Worksheets(1).UsedRange
    
    '// �e�V�[�g��A1�Z�����擾
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
    
    Debug.Print ("���v : " & sum)
    
      '�I�����Ԏ擾
  endTime = Timer
 
  '�������ԕ\��
  processTime = endTime - startTime
  Debug.Print ("�������ԁF" & processTime)
  
    
    '// �u�b�N�����
    Call wb.Close
    
    '// Excel�A�v���P�[�V���������
    Call ex.Application.Quit
End Sub

