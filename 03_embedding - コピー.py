
import os
os.environ["AZURE_OPENAI_ENDPOINT"] = ""    
os.environ["AZURE_OPENAI_API_KEY"]  = ''                                                
os.environ["AZURE_OPENAI_API_VERSION"]    = "2024-06-01"  # Azure OpenAI のAPIバージョン
os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"] = "text-embedding-3-small-2"

from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS  # pip install faiss-cpu が必要
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter  # langchain_community で同時インストールされる


# テキストファイルの読み込み
documents = []
for file in os.listdir("./news"):
    if file.endswith(".txt"):
        loader = TextLoader(f"./news/{file}", encoding="utf-8")
        documents.extend(loader.load()) 

# テキストの分割
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# FAISSベクトルストアの作成
embeddings = AzureOpenAIEmbeddings()
vectorstore = FAISS.from_documents(texts, embeddings) 

# ベクトルストアの保存
vectorstore.save_local("faiss_index")

print("エンベディングが完了し、インデックスが保存されました。")

