"""
チェック事項ごとに、各ＤＢの類似文章を検索し、結果をまとめる。
LLM(embeddings)を使って、類似文章を検索する。
"""

from langchain_community.vectorstores import FAISS
import polars as pl
from langchain_openai import AzureOpenAIEmbeddings


class Hikaku_jikko:
    def __init__(self, llm: AzureOpenAIEmbeddings):
        self.llm = llm

    def run(self, persist_directorys   , question_file ):

        # 質問事項を読み込む
        df_questions = pl.read_excel(question_file)
        df_questions = df_questions.select(
            pl.col('番号').cast(pl.Utf8).alias('番号')
            ,pl.col('チェック事項').cast(pl.Utf8).alias('チェック事項')
        )

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
                    print(f'処理中：{count} - {i}  ')
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

        print(df_matome)
        df_matome.write_csv('df_matome.tsv',separator='\t')

        return 'df_matome.tsv'

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
    embeddings = AzureOpenAIEmbeddings( azure_deployment=emb_azure_deployment, openai_api_version=emb_openai_api_version, openai_api_key=emb_openai_api_key, azure_endpoint=emb_azure_endpoint ) 


    persist_directorys =[ r"./faiss_kana_0102"   , r"./faiss_kk_0102" ,  r"./faiss_kk_kai_0102"]  # データベースの保存先ディレクトリ  
    question_file = '質問事項.xlsx'

    hikaku_ = Hikaku_jikko(llm=embeddings)
    file_hikaku  = hikaku_.run(persist_directorys = persist_directorys , question_file = question_file) # 一時フォルダのパスを指定 

    print(file_hikaku)
    print('end! ')



