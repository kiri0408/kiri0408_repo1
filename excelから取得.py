import pandas as pd
import numpy as np
import win32com.client

C_JBAN1 = 1
C_JBAN2 = 26
C_CAL_STA = 7
C_CAL_END = 20
R_CAL = 2

try:
    #EXCELオープン
    #▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽
    #xl = GetObject(None, "Excel.Application")
    xl = win32com.client.Dispatch("Excel.Application")
    from pathlib import Path
    abspath = str(Path(r"C:\Users\arwml\py1\99.sonota\3kakann.xlsx").resolve())
    wb = xl.Workbooks.Open(abspath, UpdateLinks=0, ReadOnly=True)  # 読み取り専用の場合は  ReadOnly=True

    # for i in range(0, wb.Worksheets.Count):
    #     print(wb.Worksheets[i].name)

    #ws1 = wb.Sheets("Sheet1")
    xl.DisplayAlerts = False # 警告を非表示
    xl.Visible = False  #非表示
    #△△△△△△△△△△△△△△△△△△△△△△△
except:
    print("エラー発生しました")
    #EXCEL終了処理
    #▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽
    xl.DisplayAlerts = True # 警告を表示
    xl.Visible = True       # 表示
    #△△△△△△△△△△△△△△△△△△△△


jban_list=[]
jban=''
hiduke_list = []


for i_sheet in range(0, wb.Worksheets.Count):

    #対象シートをws1へセット
    ws1 = wb.Sheets(wb.Worksheets[i_sheet].name)

    #所定シートでない場合はcontinueする
    if ws1.Cells.Item(1,1).Value != 'c1':  
        continue

    #対象シートをｄｆへ読み込み
    df=pd.read_excel(r"C:\Users\arwml\py1\99.sonota\3kakann.xlsx", sheet_name=wb.Worksheets[i_sheet].name)
    df=df.fillna('')

    #ｄｆから １行ずつ J番号を抽出する
    for row in range(1,len(df)):

        print(f'Ｊ番号を読み取り中          : {wb.Worksheets[i_sheet].name}  行:{row}  ')

        #J番記載 １列目
        df.iloc[row,C_JBAN1-1] = str(df.iloc[row,C_JBAN1-1])  #文字型に変換する
        if df.iloc[row,C_JBAN1-1] =='' :                         #セルが空文字の場合
            df.iloc[row,C_JBAN1-1] = df.iloc[row-1,C_JBAN1-1]    #この行は上の行のセルを引き継ぐとみなし値をコピーする
        for i in range(len(df.iloc[row,C_JBAN1-1])):  #iはセル内の文字を１文字ずつ判定するカーソル 
            if df.iloc[row,C_JBAN1-1][i] =='J'  and i+5 <= len(df.iloc[row,C_JBAN1-1]) :  #文字Jが存在し、かつ５文字確保できる場合
                jban = df.iloc[row,C_JBAN1-1][i:i+5]  #そこから５文字をJ番として抽出する
                i=i+5                                 #J番5桁分 カーソルを進める
                jban_list.append([jban,str(wb.Worksheets[i_sheet].name) +'_'+ str(row+2)])          #J番リストへ追加。  row+2 はexcel表記への調整

        #J番記載 ２列目
        df.iloc[row,C_JBAN2-1] = str(df.iloc[row,C_JBAN2-1])  #文字型に変換する
        if df.iloc[row,C_JBAN2-1] =='' :                         #セルが空文字の場合
            df.iloc[row,C_JBAN2-1] = df.iloc[row-1,C_JBAN2-1]    #この行は上の行のセルを引き継ぐとみなし値をコピーする
        for i in range(len(df.iloc[row,C_JBAN2-1])):  #iはセル内の文字を１文字ずつ判定するカーソル 
            if df.iloc[row,C_JBAN2-1][i] =='J'  and i+5 <= len(df.iloc[row,C_JBAN2-1]) :  #文字Jが存在し、かつ５文字確保できる場合
                jban = df.iloc[row,C_JBAN2-1][i:i+5]  #そこから５文字をJ番として抽出する
                i=i+5                                 #J番5桁分 カーソルを進める
                jban_list.append([jban,str(wb.Worksheets[i_sheet].name) +'_'+ str(row+2)])          #J番リストへ追加。  row+2 はexcel表記への調整


    # 計画・実績取得のため先ずは 日付行の空セルに日付をセットする
    for j in range(1,len(df.columns)):
        if df.iloc[0,j] == '' :              # 日付空白の場合
            df.iloc[0,j] = df.iloc[0,j-1]    # 左の列の日付をコピーする 

    # ws1から１行ずつ計画・実績を抽出
    for row in range(R_CAL+1, len(df)+2):
        print(f'計画日・実績日を読み取り中  : {wb.Worksheets[i_sheet].name}  行:{row}  ')
        for col in range(C_CAL_STA,C_CAL_END):
            if ws1.Range(ws1.cells(row,col), ws1.cells(row,col)).Interior.Color == 12566463.0 :  #12566463.0  灰色 
                hiduke_list.append([str(wb.Worksheets[i_sheet].name) +'_'+ str(row),df.iloc[0,col-1],'1計画'])
            elif ws1.Range(ws1.cells(row,col), ws1.cells(row,col)).Interior.Color == 65535.0 :  #65535.0  黄色 
                hiduke_list.append([str(wb.Worksheets[i_sheet].name) +'_'+ str(row),df.iloc[0,col-1],'2実績'])



#print(jban_list)
#ｄｆ変換
df_jban = pd.DataFrame(    data=np.array(jban_list),    columns=['J番', '行']       )
df_jban = df_jban[ ~df_jban.duplicated() ].reset_index(drop=True)  #重複を削除

#ｄｆ変換
df_hiduke = pd.DataFrame(    data=np.array(hiduke_list),    columns=['行', '日付', '区分']       ) 
df_hiduke = df_hiduke[ ~df_hiduke.duplicated() ].reset_index(drop=True)  #重複を削除
#print(df_hiduke)

#J番号と計画・実績データをmergeする
df_meisai = pd.merge(df_jban,df_hiduke,left_on='行', right_on='行',how='left') 

#J番ごとの計画日の初日と最終日を集計する
df_meisai_keikaku = df_meisai[df_meisai['区分']=='1計画'] 
df_meisai_keikaku_min = df_meisai_keikaku[['J番','日付']].groupby(['J番']).min().sort_values(['J番']).rename(columns={'日付':'計画初日'})
df_meisai_keikaku_max = df_meisai_keikaku[['J番','日付']].groupby(['J番']).max().sort_values(['J番']).rename(columns={'日付':'計画最終日'})

#J番ごとの実績日の初日と最終日を集計する
df_meisai_jisseki = df_meisai[df_meisai['区分']=='2実績'] 
df_meisai_jisseki_min = df_meisai_jisseki[['J番','日付']].groupby(['J番']).min().sort_values(['J番']).rename(columns={'日付':'実績初日'})
df_meisai_jisseki_max = df_meisai_jisseki[['J番','日付']].groupby(['J番']).max().sort_values(['J番']).rename(columns={'日付':'実績最終日'})

#抽出されたJ番に対して、計画・実績の初日・最終日をleft joinする。 
df_jban_only = df_jban['J番']
df_jban_only = df_jban_only[ ~ df_jban_only.duplicated()].reset_index(drop=True) #重複を削除
df_kekka = pd.merge(df_jban_only,df_meisai_keikaku_min,on='J番',how='left')
df_kekka = pd.merge(df_kekka    ,df_meisai_keikaku_max,on='J番',how='left')
df_kekka = pd.merge(df_kekka    ,df_meisai_jisseki_min,on='J番',how='left')
df_kekka = pd.merge(df_kekka    ,df_meisai_jisseki_max,on='J番',how='left')
print(df_kekka)

xl.DisplayAlerts = True # 警告を表示
xl.Visible = True       # 表示
