
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "user",
            [
                {"type": "text", "text": (
                    "この画像は文書をjpegにしたものですのでテキストに変換できます。すべての内容を余すことなくmarkdown形式のテキストで出力してください。"
                    "テーブル表が含まれている場合は、その内容もmarkdown形式に含めてください。"
                    "あなたはテーブル表の数値を間違うことがあります。落ち着いてしっかりと正しい数値を読み取ってください。"
                    "数値の間違いはゆるされません。数値は必ず正しい値で出力してください"
                    "要約は不要です。そのままの表現でmarkdown形式に含めて出力してください。"
                    "ただし、テーブル表はmeltしたロング型で出力してください"
                )},
                
                {"type": "image_url", "image_url": {"url": "{image_url}"}},
            ],
        ),
    ]
)

import base64



with open(  r'output18.jpg', 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    image_url = f'data:image/jpg;base64,{encoded_string}'

prompt_value = prompt.invoke({"image_url": image_url})

model = ChatOpenAI(model="gpt-4o", temperature=0)
ai_message = model.invoke(prompt_value)
print(ai_message.content)

with open('imageread.txt',mode='w', encoding='utf-8') as f:
    f.write(ai_message.content) 