import openai
        
openai.api_key = "sk-JclJ51fuaV4PcDZVibljARWT3BlbkFJLilcV5GRVK03QhHod3XH"
model_engine = "text-davinci-003"
prompt = '開発規模が小さい個人用ツールの場合、ソフトウェア仕様書なしで開発してもいい？'

completion = openai.Completion.create(
engine=model_engine,
prompt=prompt,
max_tokens=1024,
n=1,
stop=None,
temperature=0.5,
)

response = completion.choices[0].text
print(response)