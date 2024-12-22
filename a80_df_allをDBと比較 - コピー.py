# import chromadb
# from chromadb.config import Settings
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from langchain_chroma import Chroma
from langchain.schema import Document
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
import polars as pl

page_start=1
page_end = 100

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

persist_directory = "./chroma_db_1222a"  # データベースの保存先ディレクトリ  


# PDFの一覧チャンクデータを読み込み
df_all = pl.read_csv(r'doc_raw\df_all.tsv',separator='\t',dtypes= [pl.Utf8, pl.Utf8, pl.Utf8, pl.Utf8, pl.Utf8, pl.Float64, pl.Utf8, pl.Utf8, pl.Utf8])
print(df_all)



# Document クラスのリストを作成
# docs = []
# for i in range(len(df_all)):
#     if df_all[i,'delete'] != 'del' and len(df_all[i,'emb'] )>5 :
#         docs.append(Document(  page_content=df_all[i,'emb'] , metadata={"memo":df_all[i,'meta']}))

# print(docs[:3])
# print( f' 埋め込み対象のチャンク数： {len(docs)} ' )


################ エンベディング処理  #########################
# db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)   # ★★★★★★★★★★★★★★  処理の都度 同じデータが追加されるので注意。  更新ではない。  ★★★★★★★★★★★★★★★
# print("Chroma DBにデータを追加しました。",persist_directory)


#####################  DB読み込み  ########################
db = Chroma(persist_directory=persist_directory,embedding_function=embeddings)



######################### DB比較 ###########################

kensaku_kekka = []


for i in range(page_start,page_end):

    query = df_all[i,'emb']
    index = df_all[i,'index']

    if  df_all[i,'delete'] != 'del' and  len(query) > 5 :

        print(f'処理中：{i}  ')
        results = db.similarity_search_with_score(query=query,k=3)   #scoreは低い方が類似度が高い。 

        for doc , score in results:

            try:
                meta_memo  =  doc.metadata['memo']
            except:
                meta_memo = ''

            #print(f' 文：{doc.page_content}  メモ：{meta_memo} 類似度：{score:.4f}             ')
            kensaku_kekka.append([ index,  doc.page_content , meta_memo, score]) 


df_kensaku_kekka = pl.DataFrame( kensaku_kekka , strict=False).transpose()
df_kensaku_kekka = df_kensaku_kekka.select(
    pl.col('column_0').str.strip_chars().cast(pl.Float64, strict=False).alias('index')  
    ,pl.col('column_1').alias('資料B_本文_emb')
    ,pl.col('column_2').alias('資料B_項番')
    ,pl.col('column_3').alias('誤差')
)
df_kensaku_kekka = df_kensaku_kekka.with_columns(pl.lit('').alias('資料B_本文'))
for i in range(len(df_kensaku_kekka)):
    text = df_kensaku_kekka[i,'資料B_本文_emb']
    lines = text.split("\n")  # 改行で分割
    df_kensaku_kekka[i,'資料B_本文'] = "\n".join(lines[1:])  # 2行目以降を再結合

df_kensaku_kekka.write_csv('df_kensaku_kekka.tsv',separator='\t')
print(df_kensaku_kekka) 

df_all = df_all.join(df_kensaku_kekka,on='index',how='left')

for i in range(1,len(df_all)):
    if df_all[i,'index'] == df_all[i-1,'index']:
        df_all[i,'midashi1'] = ''
        df_all[i,'midashi2'] = ''
        df_all[i,'midashi3'] = ''
        df_all[i,'midashi4'] = ''
        df_all[i,'content'] = ''

df_all = df_all.select(['midashi1','midashi2','midashi3','midashi4','content','資料B_本文','誤差','資料B_項番','index','delete','emb','meta','資料B_本文_emb'])

df_all.write_csv('df_all_kensaku_kekka.tsv',separator='\t')


