

"""
PDFを1ページごとにテキスト化したものを整える。 *WT_cleaned.txt ファイルを作成する。
LLM pydanticを使うことでヘッダー、フッターの正規表現を変数に取得。 
ヘッダー、フッター、文頭の空行、文末の空行を削除する。
100ページで5秒以内

"""


import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import time
import re
import random
from pydantic import BaseModel, Field
import glob

message_human = '''
# 命令文  : 本文1～本文5を参照し、最初数行に繰り返し出てくるヘッダー行と最後数行に繰り返し出てくるフッター行を抽出してください。 複数あれば複数抽出してください。 
           それらヘッダー行・フッター行の正規表現に最も適切なものを選択肢1～選択肢3から選択してください。
# 出力    : 選択肢（1,2,3）から1つを選択し、その数値と、選択した理由を出力してください。
# 補足    : ・先頭数行や最終数行で、数字と記号のみの行もヘッダー行・フッター行として扱う。 
            ・空白が入りそうな箇所は積極的に \s* を使う。 
            ・40文字以上の行は、ヘッダー行・フッター行として扱わない。
            ・ヘッダー行・フッター行は、本文の先頭や最後のみに繰り返し出てくるもので、かつ、 基本的に全ての本文に出現しているもとする。 

# 選択肢1
{HeaderFooter1}

# 選択肢2
{HeaderFooter2}

# 選択肢3
{HeaderFooter3}

# 本文1
{str_honbun1}

# 本文2
{str_honbun2}

# 本文3
{str_honbun3}

# 本文4
{str_honbun4}

# 本文5
{str_honbun5}

'''


class Sentaku(BaseModel):
    sentaku: int = Field(..., description="選択肢") 
    riyu : str = Field(..., description="選択した理由")


class HeaderFootersSentaku: 
    def __init__(self, llm: AzureChatOpenAI):
        self.llm = llm.with_structured_output(Sentaku)

    def read_random_wt_file(self, folder_path):

        file_paths = glob.glob(os.path.join(folder_path, "output[0-9][0-9][0-9][0-9].txt"))

        random_sample = random.sample(file_paths, 5)
        
        list_content = []
        for file_path in random_sample:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                list_content.append(content)
        return  list_content




    def remove_matching_lines(self, text, patterns):
        # 各行を分割
        lines = text.split('\n')
        
        # パターンにマッチしない行だけを保持
        filtered_lines = [line for line in lines if not any(re.match(pattern, line) for pattern in patterns)]
        
        # 行を再結合
        return '\n'.join(filtered_lines)

    # 文頭の空行を削除する
    def remove_leading_lines(self,text):
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if not re.match(r'^\s*$', line):
                return '\n'.join(lines[i:])
        return ''  # すべての行が空白の場合

    # 文末の空行を削除する
    def remove_trailing_empty_lines(self,text):
        lines = text.splitlines()
        while lines and re.match(r'^\s*$', lines[-1]):
            lines.pop()
        return '\n'.join(lines)

    # フォルダ内の全ファイルからヘッダー、フッター、文頭の空行、文末の空行を削除
    def delete_header_footer(self, folder_path, patterns_to_remove):
        
        # *_WT.txt パターンに一致するファイルをフィルタリング
        #wt_files = [f for f in all_files if f.endswith('_WT.txt')]
        file_paths = glob.glob(os.path.join(folder_path, "output[0-9][0-9][0-9][0-9].txt"))
        for file_path in file_paths:
            # ファイルの完全なパスを作成
            #file_path = os.path.join(folder_path, wt_file)
            
            try:
                # ファイルの内容を読み込む
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # ヘッダー、フッターを削除
                content = self.remove_matching_lines(content, patterns_to_remove)

                # 文頭の空行を削除
                content = self.remove_leading_lines(content)
                
                # 文末の空行を削除
                content = self.remove_trailing_empty_lines(content)

                # ファイルを上書き保存
                file_path_new = file_path.replace('.txt', '_WT_cleaned.txt')
                with open(file_path_new, 'w', encoding='utf-8') as file:
                    file.write(content)
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
    
    def _read_and_combine_files(self, folder_temp: str) -> str:
        # *WT_cleaned.txtパターンに一致するファイルを取得し、ソート
        file_pattern = os.path.join(folder_temp, '*WT_cleaned.txt')
        files = sorted(glob.glob(file_pattern))
        
        combined_text = ""
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                combined_text += f.read() + "\n"
        
        return combined_text

    def run(self, folder_temp:str , HeaderFooter1:list[str], HeaderFooter2:list[str], HeaderFooter3:list[str]   ) -> list[str]:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたはテキストを分析する優秀なアシスタントです。"),
            ("human" , message_human),
            ])


        # ランダムに５つのファイルを選択して読み込む
        sample_txt = self.read_random_wt_file(folder_temp)
        #print(sample_txt)

        chain = prompt | self.llm 
        sentaku : Sentaku = chain.invoke({"str_honbun1": sample_txt[0], "str_honbun2": sample_txt[1] , "str_honbun3": sample_txt[2] , "str_honbun4": sample_txt[3] , "str_honbun5": sample_txt[4] ,"HeaderFooter1":HeaderFooter1, "HeaderFooter2":HeaderFooter2, "HeaderFooter3":HeaderFooter3})
        print('選択したもの ： ',sentaku.sentaku)
        print('選択理由 ： ',sentaku.riyu)

        if sentaku.sentaku == 1:
            HeaderFooter_sentaku = HeaderFooter1
        elif sentaku.sentaku == 2:
            HeaderFooter_sentaku = HeaderFooter2
        elif sentaku.sentaku == 3:
            HeaderFooter_sentaku = HeaderFooter3
        else:
            HeaderFooter_sentaku = "xxxxxxxxxxx"

        # フォルダ内の全ファイルからヘッダー、フッター、文頭の空行、文末の空行を削除
        self.delete_header_footer(folder_temp, HeaderFooter_sentaku)

        combined_text = self._read_and_combine_files(folder_temp)
        with open(folder_temp + r'/combined_text.txt', 'w', encoding='utf-8') as f:
            f.write(combined_text)
        print('テキストを集約、保存しました。 ' , folder_temp + r'/combined_text.txt') 



        return HeaderFooter_sentaku, sentaku.sentaku, sentaku.riyu ,combined_text

        

####################################### 単独実行用main ########################################################
if __name__ == "__main__":
    start_time = time.perf_counter()

    folder_temp = r'./doc_raw/kk_0102/'   # フォルダ内の全てのWT.txtからヘッダー、フッター、文頭の空行、文末の空行を削除し、同フォルダに WT_cleaned.txtを作成する 
    folder_temp = r'./kana_20250104_221732/'   # フォルダ内の全てのWT.txtからヘッダー、フッター、文頭の空行、文末の空行を削除し、同フォルダに WT_cleaned.txtを作成する 

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
    model = AzureChatOpenAI(  deployment_name=deployment_name, openai_api_version=openai_api_version, openai_api_key=openai_api_key, azure_endpoint=azure_endpoint, temperature=0 )

    # ランダムな５つのファイルからヘッダー、フッターの正規表現を取得
    hdft_sentaku = HeaderFootersSentaku(llm=model)
    HeaderFooter_sentaku, bango_sentaku , riyu ,combined_text = hdft_sentaku.run(folder_temp =folder_temp , HeaderFooter1=['^\\s*1\\s*[-－aaa]\\s*\\d+\\s*$', '^\\s*\\d+\\s*[-－bbb]\\s*\\d+\\s*$'], HeaderFooter2=['^\\s*1\\s*－－－\\s*\\d+\\s*$'], HeaderFooter3=['^\\s*1\\s*－\\s*\\d+\\s*$'])
    print(HeaderFooter_sentaku, bango_sentaku, riyu,'\n\n' ,combined_text[:100]  )

    print(f"--- Finished ---  開始から{time.perf_counter() - start_time :.2f}秒 ")

