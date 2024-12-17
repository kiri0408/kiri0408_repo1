
import polars as pl 
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

from langchain_chroma import Chroma
persist_directory = "./chroma_db"  # 保存先ディレクトリ

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# query = "AWSのS3からデータを読み込むためのDocument loaderはありますか？"
# vector = embeddings.embed_query(query)
# print(len(vector))
# print(vector)

if True:
    ############# ロード #############
    from langchain_community.document_loaders import DirectoryLoader
    loader = DirectoryLoader(
        path="./doc_raw",
        glob="**/*kk.txt",
        show_progress=True,
        use_multithreading=True
    )

    import sys
    sys.path.append(r'C:\py\80_agents\Release-24.08.0-0\poppler-24.08.0\Library\bin')


    raw_docs = loader.load()
    print(len(raw_docs))

    ############## チャンク分割 ##############
    from langchain_text_splitters import CharacterTextSplitter

    text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=96)

    docs = text_splitter.split_documents(raw_docs)
    print(len(docs))

    #print(docs[0].page_content)

    list_doc =[]
    for i in range(len(docs)):
        try:
            list_doc.append([ docs[i].page_content , docs[i].metadata['source']])
        except:
            pass
    print(list_doc)
    df_doc = pl.DataFrame(list_doc)
    df_doc = df_doc.transpose()
    df_doc.write_excel('df_doc_kk.xlsx')
    print(df_doc)

    ################ ベクトルDB保存 ###################

    #db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    #db.persist() # データベースを明示的に保存


db = Chroma(persist_directory=persist_directory,embedding_function=embeddings)
retriever = db.as_retriever()

model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_template('''\
以下の仕様Aに記載の内容に対し、仕様Bでの変更を列挙してください。
 - 仕様の変更 
 - 規格の変更
 - 寸法、温度などの数値の変更 

仕様A: {question}                                          
                                          
仕様B: """
{context}
"""


''')
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

#df_doc = df_doc.with_columns(pl.lit('').alias('推測'))
 
list_kekka = []
for i in range(3):

    ##################  rerieve #################
    print(f'--------------------------------{str(i)}-------------------------------------------')
    query = df_doc[i,0]
    print(query)
    context_docs = retriever.invoke(query)
    print(f"len = {len(context_docs)}")

    ####################################### 回答生成 ####################################################

    output = chain.invoke(query)
    print(output)
    for doc in context_docs:
        list_kekka.append([str(i), query, output, doc.page_content]) 


df_kekka = pl.DataFrame(list_kekka)
df_kekka = df_kekka.transpose()
df_kekka.write_excel('df_kekka.xlsx')

