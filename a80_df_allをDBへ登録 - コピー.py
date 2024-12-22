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

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

persist_directory = "./chroma_db_1222a"  # データベースの保存先ディレクトリ  

# PDFの一覧チャンクデータを読み込み
df_all = pl.read_csv(r'doc_raw\df_all.tsv',separator='\t',dtypes= [pl.Utf8, pl.Utf8, pl.Utf8, pl.Utf8, pl.Utf8, pl.Float64, pl.Utf8, pl.Utf8, pl.Utf8])
print(df_all)

# Document クラスのリストを作成
docs = []
for i in range(len(df_all)):
    if df_all[i,'delete'] != 'del' and len(df_all[i,'emb'] )>5 :
        docs.append(Document(  page_content=df_all[i,'emb'] , metadata={"memo":df_all[i,'meta']}))

print(docs[:3])
print( f' 埋め込み対象のチャンク数： {len(docs)} ' )


################ エンベディング処理  #########################
# db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)   # ★★★★★★★★★★★★★★  処理の都度 同じデータが追加されるので注意。  更新ではない。  ★★★★★★★★★★★★★★★
# print("Chroma DBにデータを追加しました。",persist_directory)


#####################  DB読み込み  ########################
db = Chroma(persist_directory=persist_directory,embedding_function=embeddings)
query='ケーブル又はバスダクトが防火区画等を貫通する場合は'
results = db.similarity_search_with_score(query=query,k=3)   #scoreは低い方が類似度が高い。 

for doc , score in results:
   
    try:
        meta_source = doc.metadata['source']
    except:
        meta_source=''
    try:
        meta_page  =  doc.metadata['page']
    except:
        meta_page = ''
    try:
        meta_memo  =  doc.metadata['memo']
    except:
        meta_memo = ''

    print(f' 文：{doc.page_content}  ソース：{meta_source}  ページ：{meta_page}  メモ：{meta_memo} 類似度：{score:.4f}             ')

