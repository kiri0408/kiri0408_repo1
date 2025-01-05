

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
           それらヘッダー行・フッター行の正規表現を作成してください。
# 出力    : 抽出したヘッダー行・フッター行の正規表現と、その正規表現を作成した理由・根拠を出力してください。
# 補足    : ・先頭数行や最終数行で、数字と記号のみの行もヘッダー行・フッター行として扱ってください。 
            ・空白が入りそうな箇所は積極的に \s* を使ってください。 
            ・40文字以上の行は、ヘッダー行・フッター行として扱わないでください。
            ・ヘッダー行・フッター行は、本文の先頭や最後のみに繰り返し出てくるもので、かつ、 基本的に全ての本文に出現しているものです。



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


class HeaderFooter(BaseModel):
    hdft: str = Field(..., description="ヘッダー行・フッター行の正規表現") 
    hdft_riyu: str = Field(..., description="ヘッダー行・フッター行の正規表現の理由、根拠")

class HeaderFooters(BaseModel):
    hdfts: list[HeaderFooter] = Field(  default_factory=list, description="ヘッダーまたはフッターの正規表現のリスト"      )

class HeaderFootersGenerator:
    def __init__(self, llm: AzureChatOpenAI):
        self.llm = llm.with_structured_output(HeaderFooters)


    def read_random_wt_file(self, folder_path):

        file_paths = glob.glob(os.path.join(folder_path, "output*.txt"))

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
        # フォルダ内の全ファイルを取得
        all_files = os.listdir(folder_path)
        
        # *_WT.txt パターンに一致するファイルをフィルタリング
        wt_files = [f for f in all_files if f.endswith('_WT.txt')]
        for wt_file in wt_files:
            # ファイルの完全なパスを作成
            file_path = os.path.join(folder_path, wt_file)
            
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
                file_path_new = os.path.join(folder_path, wt_file.replace('_WT.txt', '_WT_cleaned.txt'))
                with open(file_path_new, 'w', encoding='utf-8') as file:
                    file.write(content)
            except Exception as e:
                print(f"Error processing file {wt_file}: {str(e)}")
    
    def _read_and_combine_files(self, folder_temp: str) -> str:
        # *WT_cleaned.txtパターンに一致するファイルを取得し、ソート
        file_pattern = os.path.join(folder_temp, '*WT_cleaned.txt')
        files = sorted(glob.glob(file_pattern))
        
        combined_text = ""
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                combined_text += f.read() + "\n"
        
        return combined_text

    def run(self, folder_temp:str , kaisu:int) -> list[str]:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたはテキストを分析する優秀なアシスタントです。"),
            ("human" , message_human),
            ])


        # ランダムに５つのファイルを選択して読み込む
        sample_txt = self.read_random_wt_file(folder_temp)
        #print(sample_txt)

        chain = prompt | self.llm 
        hdfts : HeaderFooters = chain.invoke({"str_honbun1": sample_txt[0], "str_honbun2": sample_txt[1] , "str_honbun3": sample_txt[2] , "str_honbun4": sample_txt[3] , "str_honbun5": sample_txt[4]  })

        # 削除したい行のパターンリスト
        HeaderFooter = [hdft.hdft for hdft in hdfts.hdfts] 
        HeaderFooter_riyu = [hdft.hdft_riyu for hdft in hdfts.hdfts] 

        
        HeaderFooter = list(set(HeaderFooter))  # setを使用して重複を排除し、再びリストに変換
        print(str(kaisu),HeaderFooter) 
        print(HeaderFooter_riyu)

        # folder_tempリストの内容をファイルに出力する
        file_path = os.path.join(folder_temp, 'header_footer_' + str(kaisu)  + '.txt')
        with open(file_path, 'w' , encoding='utf-8') as f:
            for item in HeaderFooter:
                f.write(item + '\n')

        # # フォルダ内の全ファイルからヘッダー、フッター、文頭の空行、文末の空行を削除
        # self.delete_header_footer(folder_temp, HeaderFooter)

        # combined_text = self._read_and_combine_files(folder_temp)
        # with open(folder_temp + r'/combined_text.txt', 'w', encoding='utf-8') as f:
        #     f.write(combined_text)
        # print('テキストを集約、保存しました。 ' , folder_temp + r'/combined_text.txt') 

        return HeaderFooter

####################################### 単独実行用main ########################################################
if __name__ == "__main__":
    start_time = time.perf_counter()

    folder_temp = r'./doc_raw/kk_0102/'   # フォルダ内の全てのWT.txtからヘッダー、フッター、文頭の空行、文末の空行を削除し、同フォルダに WT_cleaned.txtを作成する 
    folder_temp = r'./kana_20250104_204709/'   # フォルダ内の全てのWT.txtからヘッダー、フッター、文頭の空行、文末の空行を削除し、同フォルダに WT_cleaned.txtを作成する 

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
    hdft_generator = HeaderFootersGenerator(llm=model)
    hdfts = hdft_generator.run(folder_temp =folder_temp , kaisu=3)

    print(f"--- Finished ---  開始から{time.perf_counter() - start_time :.2f}秒 ")

