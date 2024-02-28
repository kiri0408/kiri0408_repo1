
import os
os.environ["OPENAI_API_KEY"] = ""


import chainlit as cl
#from langchain.chat_models import ChatOpenAI
#from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
#from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA  #← RetrievalQAをインポートする

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
#from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma

embeddings = OpenAIEmbeddings( model="text-embedding-ada-002" )

chat = ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate(template="""文章を元に質問に答えてください。 

文章: 
{document}

質問: {query}
""", input_variables=["document", "query"])

database = Chroma( persist_directory="./.data",  embedding_function=embeddings )

retriever = database.as_retriever() #← データベースをRetrieverに変換する


qa = RetrievalQA.from_llm(  #← RetrievalQAを初期化する
llm=chat,  #← Chat modelsを指定する
retriever=retriever,  #← Retrieverを指定する
return_source_documents=True  #← 返答にソースドキュメントを含めるかどうかを指定する
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="準備ができました！メッセージを入力してください！").send()


@cl.on_message
async def on_message(input_message:str ):
    print("入力されたメッセージ: " + input_message.content )

    # documents = database.similarity_search(input_message) #← input_messageに変更
    # documents_string = ""
    # for document in documents:
    #     documents_string += f"""
    # ---------------------------
    # {document.page_content}
    # """
    # result = chat([
    #     HumanMessage(content=prompt.format(document=documents_string,     query=input_message)) #← input_messageに変更
    # ])

    result = qa(input_message.content)

    for i in range(len(result)):
        await cl.Message(content='--------------------------   参照した文章 No. ' + str(i+1) + '-------------------------------------').send() #← チャットボットからの返答を送信する
        await cl.Message(content=result["source_documents"][i].metadata['source']).send() #← チャットボットからの返答を送信する
        await cl.Message(content=result["source_documents"][i].page_content).send() #← チャットボットからの返答を送信する

    await cl.Message(content='--------------------------------------------------回答--------------------------------------------------').send() #← チャットボットからの返答を送信する
    await cl.Message(content=result["result"]).send() #← チャットボットからの返答を送信する


    