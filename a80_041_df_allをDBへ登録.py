
"""
df_allのチャンクを元に、プログレスバーを表示しながら メタデータも含めてベクトル化。 DBへ保存する
100ページで3分くらい？ 
LLM(embeddings)を使ってベクターデータを作成する。
"""

from langchain_openai import AzureOpenAIEmbeddings
from langchain.schema import Document
import polars as pl
from langchain_community.vectorstores import FAISS
from tqdm import tqdm

class Embedding_jikko:
    def __init__(self, llm):
        self.llm = llm


    def run(self, folder_temp, df_all):

        # Document クラスのリストを作成
        docs_chunks = []
        for i in range(len(df_all)):
            if df_all[i, 'delete'] != 'del' and len(df_all[i, 'emb']) > 5:
                docs_chunks.append(Document(page_content=df_all[i, 'emb'], metadata={"memo": df_all[i, 'meta']})) 
        #print(df_all[10:15])
        print('埋め込み用のドキュメントクラスを作成しました')
        print("ドキュメント数：", len(docs_chunks))
        #print("型", type(docs_chunks[15]))
        #print("データサンプル：", docs_chunks[15]) 

        print('ベクトル化を実行中・・・') 
        faiss_db = None
        with tqdm(total=len(docs_chunks), desc="documents 抽出") as pbar:
            for d in docs_chunks:
                if faiss_db:
                    faiss_db.add_documents([d])
                else:
                    faiss_db = FAISS.from_documents([d], self.llm)
                pbar.update(1)

        #ベクトル化データを保存
        folder_db = folder_temp + r"_faiss_db"
        faiss_db.save_local(folder_db)
        print('DBフォルダに保存しました : ',folder_db)

        return folder_db


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
    
    emb_ = Embedding_jikko(llm=embeddings)

    #kana 
    # df_all = pl.read_csv(r'./kana_20250104_154214/df_all.tsv',separator='\t',dtypes= [pl.Utf8, pl.Utf8, pl.Utf8, pl.Utf8, pl.Utf8, pl.Float64, pl.Utf8, pl.Utf8, pl.Utf8])
    # folder_db  = emb_.run(folder_temp = r'./kana_20250104_154214_faiss_db_full2' , df_all = df_all) # 一時フォルダのパスを指定 

    #kk
    # df_all = pl.read_csv(r'./kk_20250105_101542/df_all.tsv',separator='\t',dtypes= [pl.Utf8, pl.Utf8, pl.Utf8, pl.Utf8, pl.Utf8, pl.Float64, pl.Utf8, pl.Utf8, pl.Utf8])
    # folder_db  = emb_.run(folder_temp = r'./kk_20250105_101542_2' , df_all = df_all) # 一時フォルダのパスを指定 

    #kk_kai
    df_all = pl.read_csv(r'./kk_kai_20250104_193658/df_all.tsv',separator='\t',dtypes= [pl.Utf8, pl.Utf8, pl.Utf8, pl.Utf8, pl.Utf8, pl.Float64, pl.Utf8, pl.Utf8, pl.Utf8])
    folder_db  = emb_.run(folder_temp = r'./kk_kai_20250104_193658_2' , df_all = df_all) # 一時フォルダのパスを指定 

    print(folder_db)
    print('end! ')



