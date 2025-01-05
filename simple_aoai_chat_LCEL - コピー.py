#from openai import AzureOpenAI



from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = AzureChatOpenAI(
    deployment_name="gpt-4o-3",
    temperature=0,
    #max_tokens=800
)

prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは優秀なお笑い芸人です。"),
        ("human", "{user_message}")
])


str_user = "日本の首相はだれ？"

formatted_prompt = prompt.format_messages(user_message=str_user)
for message in formatted_prompt:
    print(f"{message.type}: {message.content}")  #LLMに渡されるプロンプト

chain = prompt | model | StrOutputParser()
response = chain.invoke({"user_message": str_user})   

print(response)
print('end!')