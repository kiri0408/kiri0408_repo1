import os
os.environ["OPENAI_API_KEY"] = ""


#from langchain.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import PyMuPDFLoader
#from langchain.embeddings import OpenAIEmbeddings  #← OpenAIEmbeddingsをインポート
#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

from langchain.text_splitter import SpacyTextSplitter
#from langchain.vectorstores import Chroma  #← Chromaをインポート
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import Docx2txtLoader

import glob
from langchain.text_splitter import CharacterTextSplitter

embeddings = OpenAIEmbeddings( #← OpenAIEmbeddingsを初期化する
    model="text-embedding-ada-002" #← モデル名を指定
    #model="text-embedding-3-small" #← モデル名を指定  '24/2/23  model not found 
)

database = Chroma(  #← Chromaを初期化する
    persist_directory="./.data",  #← 永続化データの保存先を指定
    #persist_directory="./.data_e3small",  #← 永続化データの保存先を指定
    embedding_function=embeddings  #← ベクトル化するためのモデルを指定
)

# filepath=r'.元ドキュメント\sample.pdf'
# loader = PyMuPDFLoader(filepath)

#filepath=r'.元ドキュメント\Book2_.xlsx'
#loader = UnstructuredExcelLoader(filepath)

if False:
    #指定フォルダから ファイル名の一覧を取得 
    path = r"C:\py\68_langchain\.元ドキュメント\*.xlsx"
    file_list = glob.glob(path)

    for filepath in file_list:

        print(filepath)

        loader = UnstructuredExcelLoader(filepath)

        documents = loader.load()

        text_splitter = SpacyTextSplitter(
            chunk_size=300, 
            pipeline="ja_core_news_sm"
        )
        splitted_documents = text_splitter.split_documents(documents)
        print(splitted_documents)


        database.add_documents(  #← ドキュメントをデータベースに追加
            splitted_documents,  #← 追加するドキュメント
        )



if True :
    #指定フォルダから ファイル名の一覧を取得 
    path = r"C:\py\68_langchain\.元ドキュメント\三菱*.docx"
    file_list = glob.glob(path)

    for filepath in file_list:

        print(filepath)

        #loader = Docx2txtLoader(filepath)
        loader = UnstructuredWordDocumentLoader(filepath)

        documents = loader.load()

        # text_splitter = SpacyTextSplitter(    #SpacyTextSplitterは長い文章はエラーになる
        #     chunk_size=200, 
        #     pipeline="ja_core_news_sm"
        # )
        text_splitter = CharacterTextSplitter(
            separator = "\n\n",  # セパレータ
            chunk_size = 200,  # チャンクの文字数
            chunk_overlap = 0,  # チャンクオーバーラップの文字数
        )


        splitted_documents = text_splitter.split_documents(documents)
        for splitted_document in splitted_documents:
            try:
                source = splitted_document.metadata.get('source',None)
                filename = os.path.splitext( os.path.basename(source))[0]
                splitted_document.page_content = filename + ':' + '\n' + splitted_document.page_content   # チャンクの１行目に「（ファイル名）：」を付与している。 検索向上のため。 
            except:
                pass
        print(splitted_documents)


        database.add_documents(  #← ドキュメントをデータベースに追加
            splitted_documents,  #← 追加するドキュメント
        )

print("データベースの作成が完了しました。") #← 完了を通知する