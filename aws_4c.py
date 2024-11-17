# 外部ライブラリをインポート
import streamlit as st
from langchain_aws import ChatBedrock
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 検索手段を指定
retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="TBJMBJSRJO",  # ここにナレッジベースIDを記載する
    region_name="us-east-1",
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 10}},
)

# プロンプトのテンプレートを定義
prompt = ChatPromptTemplate.from_template(
    "以下のcontextに基づいて回答してください: {context} / 質問: {question}"
)

# LLMを指定
model = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1",
    model_kwargs={"max_tokens": 1000},
)

# チェーンを定義（検索 → プロンプト作成 → LLM呼び出し → 結果を取得）
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# フロントエンドを記述
st.title("独自文書を対象とした意味検索チャットボットTEST")

# チャット履歴の初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 質問を入力
question = st.chat_input("質問を入力してください")

# 質問が入力された場合
if question:
    # チェーンを実行して回答を取得
    answer = chain.invoke(question)

    # チャット履歴に追加
    st.session_state.chat_history.append({"role": "user", "content": question})
    st.session_state.chat_history.append({"role": "assistant", "content": answer})

# チャット履歴を時系列で表示
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])
