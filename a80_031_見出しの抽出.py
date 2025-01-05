
"""
PDFを1ページごとにテキスト化した *WT_cleaned.txt ファイルを集約。 df_shuyaku.txt ファイルを作成する。
LLM pydanticを使うことで ｻﾝﾌﾟﾙ5ページから 見出し、箇条書きの正規表現を変数に取得。   
100ページで5秒以内

"""

from langchain_openai import AzureChatOpenAI     # Azure適用時はここを変更する
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

message_human = '''
# 依頼内容
以下の文章について、見出しを表す行と箇条書きを表す行の正規表現を抽出してください。
 - 見出しの方は、行全体としてください。つまり "^" から "$"までを抽出。 
 - 箇条書きの方は、"^"から項番までとしてください。つまり ".+$" の部分は不要。
 - 正規表現で使用する数字は、半角数字なのか全角数字なのかを区別してください。
 - 半角スペース" " が存在する可能性がある場合は "\s*" で表現してください。
 - 下の例のようにタブ区切りの一覧表で出力してください。
 
# 例
レベル	正規表現	サンプル
見出し1段目	^第[０-９\d]+\s*章\s.+$	第１章
見出し2段目	^第[０-９\d]+\s*節\s.+$	第１節
見出し3段目	^[０-９]+－[０-９]+－[０-９]+\s.+$	１－１－１
見出し4段目	^[０-９]+\s.+$	１,２
箇条書き1	^\d	1,2
箇条書き2	^[ｱ-ﾜ]	ｱ,ｲ
箇条書き3	^[a-z]	a,b

# 文章
'''

class Midashi(BaseModel):
    level: str = Field(..., description="レベル")
    seikihyogen: str = Field(..., description="正規表現")
    sample : str = Field(..., description="サンプル")

# 見出しのリストを表すデータモデル
class Midashies(BaseModel):
    midashies: list[Midashi] = Field(  default_factory=list, description="見出しと箇条書きのリスト"      )

class MidashiGenerator:
    def __init__(self, llm: AzureChatOpenAI):
        self.llm = llm.with_structured_output(Midashies)

    def run(self, combined_text: str , folder_temp:str ) -> Midashies:
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
        print('先頭N文字を元に見出し抽出中...')
        midashies : Midashies = chain.invoke({"user_message": message_human + str_text_sample})

        midashi1 = ""
        midashi2 = ""
        midashi3 = ""
        midashi4 = ""
        kajo1 = ""
        kajo2 = ""
        kajo3 = ""
        for midashi in midashies.midashies:
            print(midashi.level ,' | ' , midashi.seikihyogen ,' | ', midashi.sample) 
            match midashi.level:
                case '見出し1段目':
                    midashi1 = midashi.seikihyogen
                case '見出し2段目':
                    midashi2 = midashi.seikihyogen
                case '見出し3段目':
                    midashi3 = midashi.seikihyogen
                case '見出し4段目':
                    midashi4 = midashi.seikihyogen
                case '箇条書き1':
                    kajo1 = midashi.seikihyogen
                case '箇条書き2':
                    kajo2 = midashi.seikihyogen
                case '箇条書き3':
                    kajo3 = midashi.seikihyogen

        
        print('見出しをファイル出力') 
        midashi_kajo = "\n".join([midashi1, midashi2, midashi3, midashi4, kajo1, kajo2, kajo3]) 
        with open(folder_temp + r'/midashi.txt', 'w') as f:
            f.write(midashi_kajo)
        

        return  midashi1, midashi2, midashi3, midashi4, kajo1, kajo2, kajo3 




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

    midashi_gen = MidashiGenerator(llm=llm)
    combined_text, midashi1, midashi2, midashi3, midashi4, kajo1, kajo2, kajo3  = midashi_gen.run(folder_temp = r'./kana_20250103_183730') # 一時フォルダのパスを指定 

    print(midashi1, midashi2, midashi3, midashi4, kajo1, kajo2, kajo3)




