
"""
PDFを1ページごとにテキスト化した *WT_cleaned.txt ファイルを集約。 df_shuyaku.txt ファイルを作成する。
LLM pydanticを使うことで ｻﾝﾌﾟﾙ5ページから 見出し、箇条書きの正規表現を変数に取得。   
100ページで5秒以内

"""

from langchain_openai import AzureChatOpenAI     # Azure適用時はここを変更する
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import json

message_human = '''
# 依頼内容
以下の文章について、見出しを表す行と箇条書きを表す行の正規表現を選択肢1～3の中から選択してください。
 - 見出しの方は、行全体としてください。つまり "^" から "$"までを抽出。 
 - 箇条書きの方は、"^"から項番までとしてください。つまり ".+$" の部分は不要。
 - 正規表現で使用する数字は、半角数字なのか全角数字なのかを区別してください。
 - 半角スペース" " が存在する可能性がある場合は "\s*" で表現してください。
  - 見出し4段目がない場合は、見出し4段目の行は "見出しがありません。。。" とする。

 # 出力 : 選択した選択肢の番号と、その番号を選択した理由を出力してください。

# 例
レベル	正規表現	サンプル
見出し1段目	^第[０-９\d]+\s*章\s.+$	第１章
見出し2段目	^第[０-９\d]+\s*節\s.+$	第１節
見出し3段目	^[０-９]+－[０-９]+－[０-９]+\s.+$	１－１－１
見出し4段目	^[０-９]+\s.+$	１,２
箇条書き1	^\d	1,2
箇条書き2	^[ｱ-ﾜ]	ｱ,ｲ
箇条書き3	^[a-z]	a,b

# 選択肢  (各選択肢は、[見出し1段目, 見出し2段目, 見出し3段目, 見出し4段目, 箇条書き1, 箇条書き2, 箇条書き3] の順番で記載されている)
     1 : {str_midashi_kajo1}
     2 : {str_midashi_kajo2}
     3 : {str_midashi_kajo3}

# 文章
'''

class Midashi_bango(BaseModel):
    midashi_kajo_sentaku_bango: int = Field(..., description="見出し選択肢から選択した番号")
    midashi_kajo_sentaku_riyu : str = Field(..., description="見出し選択肢からその番号を選択した理由")



class MidashiSentaku:
    def __init__(self, llm: AzureChatOpenAI):
        self.llm = llm.with_structured_output(Midashi_bango)

    def run(self, combined_text: str , folder_temp:str ,midashi_kajo1:list[str] , midashi_kajo2:list[str] , midashi_kajo3:list[str]  ) :

        str_midashi_kajo1 = "\n".join(midashi_kajo1)
        str_midashi_kajo2 = "\n".join(midashi_kajo2)
        str_midashi_kajo3 = "\n".join(midashi_kajo3)


        str_text_sample = combined_text[0:30000]  #Azure OpenAI ServiceのGPT-4o APIは、約128,000トークンまでの入力を処理できます。  1トークンは、通常、1文字です。  ただし、日本語の場合、1文字が複数のトークンに分割されることがあります。  そのため、日本語の場合、128,000トークンは、約40,000文字に相当します。
        prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    "あなたは本文中の見出しと箇条書きを抽出する専門家です。",
                ),
                (
                    "human",
                    "{user_message}"
                ),
            ])
        chain = prompt | self.llm 

        midashi_bango_ : Midashi_bango = chain.invoke({  "str_midashi_kajo1" : str_midashi_kajo1 ,"str_midashi_kajo2" : str_midashi_kajo2   ,"str_midashi_kajo3" : str_midashi_kajo3  ,"user_message": message_human + str_text_sample})

        print('選択した番号： ', midashi_bango_.midashi_kajo_sentaku_bango)
        print('選択した理由： ' , midashi_bango_.midashi_kajo_sentaku_riyu)
        if midashi_bango_.midashi_kajo_sentaku_bango == 1:
            midashi_kajo_sentaku = midashi_kajo1
        elif midashi_bango_.midashi_kajo_sentaku_bango == 2:
            midashi_kajo_sentaku = midashi_kajo2
        elif midashi_bango_.midashi_kajo_sentaku_bango == 3:
            midashi_kajo_sentaku = midashi_kajo3

        
        
        #print('見出しをファイル出力') 
        #midashi_kajo = "\n".join([midashi1, midashi2, midashi3, midashi4, kajo1, kajo2, kajo3]) 
        #file_temp = folder_temp + r'/midashi_' +str(kaisu) +'.txt'
        # with open(file_temp, 'w') as f:
        #     f.write(midashi_kajo)
        

        return midashi_kajo_sentaku , midashi_bango_.midashi_kajo_sentaku_bango, midashi_bango_.midashi_kajo_sentaku_riyu




######################### 単独実行用main #############################
if __name__ == "__main__":
    

    # 設定ファイルからデータを読み込む
    import json
    with open('a80.json', 'r', encoding='utf-8') as file:
        dict_ = json.load(file)
    deployment_name=dict_['deployment_name']
    azure_endpoint=dict_['azure_endpoint']
    openai_api_key=dict_['openai_api_key']
    openai_api_version=dict_['openai_api_version']
    emb_azure_deployment=dict_['emb_azure_deployment']
    emb_azure_endpoint=dict_['emb_azure_endpoint']
    emb_openai_api_key=dict_['emb_openai_api_key']
    emb_openai_api_version=dict_['emb_openai_api_version']

    llm = AzureChatOpenAI(  deployment_name=deployment_name, openai_api_version=openai_api_version, openai_api_key=openai_api_key, azure_endpoint=azure_endpoint, temperature=0 )

    with open('kana_20250104_221732/combined_text.txt', 'r', encoding='utf-8') as file:
        combined_text = file.read()


    midashi_sentaku = MidashiSentaku(llm=llm)
    midashi_kajo1 = ['^第[０-９\\d]+\\s*章\\s.+$', '^第[０-９\\d]+\\s*編\\s.+$', '^[０-９\\d]+－[０-９\\d]+－[０-９\\d]+\\s.+$', '見出しがありません。。。', '^\\d+', '^[ｱ-ﾜ]+', '^[a-z]+']
    midashi_kajo2 = ['^[０-９\\d]+\\s*章\\s.+$', '^第[０-９\\d]+\\s*節\\s.+$', '^[０-９\\d]+－[０-９\\d]+－[０-９\\d]+\\s.+$', '見出しがありません。。。', '^\\d+', '^[ｱ-ﾜ]+', '^[a-z]+']
    midashi_kajo3 = ['^第[０-９\\d]+\\s*章\\s.+$', '^第[０-９\\d]+\\s*節\\s.+$', '^[０-９\\d]+－[０-９\\d]+－[０-９\\d]+\\s.+$', '見出しがありません。。。', '^\\d+', '^[ｱ-ﾜ]+', '^[a-z]+']
    midashi_kajo_sentaku , midashi_kajo_sentaku_bango, midashi_kajo_sentaku_riyu  = midashi_sentaku.run( combined_text=combined_text ,folder_temp = r'./kana_20250104_221732', midashi_kajo1=midashi_kajo1, midashi_kajo2=midashi_kajo2, midashi_kajo3=midashi_kajo3  ) # 一時フォルダのパスを指定 

    print(midashi_kajo_sentaku , midashi_kajo_sentaku_bango, midashi_kajo_sentaku_riyu)




