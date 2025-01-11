"""
チェック事項ごとに、各ＤＢの類似文章を検索し、結果をまとめる。
LLM(embeddings)を使って、類似文章を検索する。
"""

from langchain_community.vectorstores import FAISS
import polars as pl
from langchain_openai import AzureOpenAIEmbeddings
import win32com.client
import tkinter as tk
from tkinter import filedialog
import os 

class Hikaku_jikko:
    def __init__(self, llm: AzureOpenAIEmbeddings):
        self.llm = llm

    def run(self, persist_directorys , columns , df_questions ):

        count = 0
        for persist_directory in persist_directorys : # データベースの保存先ディレクトリ
            count+=1

            # データベースを読み込む
            db  = FAISS.load_local(
            persist_directory, # ベクトル化データの保存先
            self.llm,          # ベクトル化モデル
            allow_dangerous_deserialization=True # デシリアライズを許可 (デフォルトはFalse)でセキュリティを向上
            )

            kensaku_kekka = []
            for i in range(len(df_questions)):
                bango = df_questions[i,'番号']
                question = df_questions[i,'チェック事項']

                if   len(question) > 5 :
                    print(f'検索中：仕様書{count} - チェック事項{i+1}  ')
                    query=question
                    results = db.similarity_search_with_score(query,k=3)   #scoreは低い方が類似度が高い。 
                    j=0
                    for doc , score in results:
                        j+=1
                        try:
                            meta_memo  =  doc.metadata['memo']
                        except:
                            meta_memo = ''

                        kensaku_kekka.append([ str(bango), str(j),  doc.page_content , meta_memo, score])  # 類似文章の番号、類似文章、メタデータ、スコアをリストに追加

            # 検索結果をデータフレームに変換                
            df_kensaku_kekka = pl.DataFrame( kensaku_kekka , strict=False)
            df_kensaku_kekka = df_kensaku_kekka.transpose()
            df_kensaku_kekka = df_kensaku_kekka.select(
                pl.col('column_0').alias('番号')
                ,pl.col('column_1').alias('枝番')
                ,pl.col('column_2').alias('本文'+str(count))
                ,pl.col('column_3').alias('項番'+str(count))
                ,pl.col('column_4').alias('誤差'+str(count))
                )

            # DBごとの検索結果を結果をまとめる
            if count==1:
                df_matome = df_questions.join(df_kensaku_kekka,on='番号',how='left')
            else:
                df_matome = df_matome.join(df_kensaku_kekka, on=['番号','枝番']  ,how='left')

        #print(df_matome)
        df_matome.write_csv('df_matome.tsv',separator='\t')

        filename =selected_file
        sheetname ='検索結果' 
        tuple=('番号','チェック事項','枝番',columns[0],'項番1','誤差1',columns[1],'項番2','誤差2',columns[2],'項番3','誤差3') 
        excel_out_col(filename=filename, sheetname=sheetname, _tuple=tuple, startRow=1, startCol=1)  
        excel_out_data(filename=filename, sheetname=sheetname, _tuple=df_matome.rows(), startRow=2, startCol=1)    # df.rows() はタプル変換 

        print('処理完了しました！')

        return True
    


# Excelへのカラム出力
def excel_out_col(filename, sheetname, _tuple, startRow, startCol):
   
    excel = win32com.client.GetObject(Class="Excel.Application")  # 開いているExcelアプリケーションへの参照を取得
    target_wb=''
    for wb in excel.Workbooks:   # 開いているワークブックの中から対象ブックを探す
        print(wb.Name)
        if wb.Name ==  os.path.basename(filename) :
            target_wb = wb
            break
    if target_wb=='' :
        print('ファイルが見つかりません', filename) 

    ws = target_wb.Worksheets(sheetname)                     #シートを取得
    ws.Range(ws.Cells(startRow,startCol),ws.Cells(startRow, startCol+len(_tuple)-1)).ClearContents()  #シートをクリア （１行目のカラムの部分）
    ws.Range(ws.Cells(startRow,startCol),ws.Cells(startRow, startCol+len(_tuple)-1)).Value = _tuple   #tuple-Excel出力  

# Excelへのデータ出力
def excel_out_data(filename, sheetname, _tuple, startRow, startCol):

    excel = win32com.client.GetObject(Class="Excel.Application") # 開いているExcelアプリケーションへの参照を取得
    for wb in excel.Workbooks:  # 開いているワークブックの中から対象ブックを探す
        if wb.Name == os.path.basename(filename) :
            target_wb = wb
            break

    ws = target_wb.Worksheets(sheetname)                          #シートを取得
    ws.Range(ws.Cells(2,1),ws.Cells(10000,100)).ClearContents()  #シートをクリア
    ws.Range(ws.Cells(startRow,startCol),ws.Cells(startRow+len(_tuple)-1, startCol+len(_tuple[0])-1)).Value = _tuple #tuple-Excel出力  len(_tuple[0])は列数を表す
    ws.Activate()                                                                                     #対象シートをアクティベート
    target_wb.Save()                                                                                  #変更を保存

def select_file():
    filename = filedialog.askopenfilename()
    if filename:
        file_label.config(text=f"選択されたファイル: {filename}")
        global selected_file
        selected_file = filename

def main():

    #persist_directorys =[ r"./kana_20250104_154214_2_faiss_db"   , r"./kk_20250105_101542_2_faiss_db" ,  r"./kk_kai_20250104_193658_2_faiss_db"]  # データベースの保存先ディレクトリ  

    question_file = selected_file

    # 質問事項を読み込む
    df_questions = pl.read_excel(question_file,sheet_name='チェック事項')
    df_questions = df_questions.select(
        pl.col('番号').cast(pl.Utf8).alias('番号')
        ,pl.col('チェック事項').cast(pl.Utf8).alias('チェック事項')
    )

    #対象仕様書を読み込む
    df_siyosho = pl.read_excel(question_file,sheet_name='仕様書')
    df_siyosho = df_siyosho.select(['対象','仕様書名','仕様書コード']) 
    siyosho_codes=[]
    siyosho_names=[]
    count=0
    for i in range(len(df_siyosho)):
        if df_siyosho[i,'対象'] =='○':
            siyosho_codes.append(df_siyosho[i,'仕様書コード'])
            siyosho_names.append(df_siyosho[i,'仕様書名'])
    print(siyosho_codes,siyosho_names)
    pass

    hikaku_ = Hikaku_jikko(llm=embeddings)
    file_hikaku  = hikaku_.run(persist_directorys = siyosho_codes[:3] , df_questions = df_questions , columns=siyosho_names[:3]) # 一時フォルダのパスを指定 

######################### 単独実行用main #############################
if __name__ == "__main__":

    # 設定ファイルからデータを読み込む
    import json
    with open('a80.json', 'r', encoding='utf-8') as file:
        dict_ = json.load(file)
    deployment_name=dict_['deployment_name']
    azure_endpoint=dict_['azure_endpoint']
    openai_api_key=dict_['openai_api_key']
    openai_api_version=dict_['openai_api_version']
    emb_azure_deployment=dict_['emb_azure_deployment']
    emb_azure_endpoint=dict_['emb_azure_endpoint']
    emb_openai_api_key=dict_['emb_openai_api_key']
    emb_openai_api_version=dict_['emb_openai_api_version']
    embeddings = AzureOpenAIEmbeddings(azure_deployment=emb_azure_deployment, 
                                       openai_api_version=emb_openai_api_version, 
                                       openai_api_key=emb_openai_api_key, 
                                       azure_endpoint=emb_azure_endpoint ) 




    # メインウィンドウの作成
    root = tk.Tk()
    root.title("PDF仕様書比較ツール")
    root.geometry("600x150")  # 希望するウィンドウサイズを設定
    root.resizable(False, False)

    # ファイル選択ボタン
    select_button = tk.Button(root, text="チェックリスト選択", command=select_file)
    select_button.pack(pady=10)

    # 選択されたファイル名を表示するラベル
    file_label = tk.Label(root, text="ファイルが選択されていません")
    file_label.pack(pady=5)

    # 実行ボタン
    execute_button = tk.Button(root, text="   検索実行   ", command=lambda:main())
    execute_button.pack(pady=10)

    # 実行結果を表示するラベル
    result_label = tk.Label(root, text="")
    result_label.pack(pady=5)

    # アプリケーションの実行
    root.mainloop()


