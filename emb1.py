
import polars as pl 
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


# query = "AWSのS3からデータを読み込むためのDocument loaderはありますか？"
# vector = embeddings.embed_query(query)
# print(len(vector))
# print(vector)


from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader(
    path="./doc_raw",
    glob="**/*.txt",
    show_progress=True,
    use_multithreading=True
)

import sys
sys.path.append(r'C:\py\80_agents\Release-24.08.0-0\poppler-24.08.0\Library\bin')


raw_docs = loader.load()
print(len(raw_docs))

from langchain_text_splitters import CharacterTextSplitter

text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=96)

docs = text_splitter.split_documents(raw_docs)
print(len(docs))

print(docs[0].page_content)

list_doc =[]
for i in range(len(docs)):
    try:
        list_doc.append([ docs[i].page_content , docs[i].metadata['source']])
    except:
        pass
print(list_doc)
df_doc = pl.DataFrame(list_doc)
df_doc = df_doc.transpose()
df_doc.write_excel('df_doc.xlsx')
print(df_doc)
from langchain_chroma import Chroma
persist_directory = "./chroma_db"  # 保存先ディレクトリ
db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
#db.persist() # データベースを明示的に保存

retriever = db.as_retriever()

query = "『立ち読み厳禁』でデビューした作家はだれ？"
print('---------------------------------------------------------------------------')
context_docs = retriever.invoke(query)
print(f"len = {len(context_docs)}")

first_doc = context_docs[0]
print(f"metadata = {first_doc.metadata}")
print(first_doc.page_content)

####################################### 以下RAG ####################################################

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template('''\
以下の文脈だけを踏まえて質問に回答してください。

文脈: """
{context}
"""

質問: {question}
''')

model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

output = chain.invoke(query)
print(output)