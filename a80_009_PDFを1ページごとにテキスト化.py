
"""
PDFを1ページごとにテキスト化する。  *WT.txt に保存する。
マルチモーダルで画像を使わずに、fitzを使ってPDFをテキスト化する。  fitzではテーブル表のデータをリスト型で構造的に抽出できる。 
LLM: AzureChatOpenAI 本文とテーブル表データを使って、本文のテーブルの整形を行う。  
100ページで15分（900秒）くらい？  （表があると遅い）

"""

import fitz  # PyMuPDF
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time
import datetime
import os
from pypdf import PdfReader as reader1
from PyPDF2 import PdfReader, PdfWriter

message_human = '''
# 目的    ：依頼本文の崩れたテーブル表の部分をきれいに整形する。
# 命令文  : 依頼本文の崩れたテーブル表の部分を テーブルデータを元に整形してください。 
# 出力    : 整形後の依頼本文のテキストのみを出力してください。 

# 補足 : 例として、本文例 を テーブルデータ例 で置き換えた結果を 変換結果例 に示しています。 

# 本文例
"""
ああああああああああああ
いいいいいいいいい
表 1.22.3 サンプル 
 項目A  項目B  
 値１  値あ   
 値２  値い   
 値３  値う   
うううううううううう
ええええええええええ
"""

# テーブルデータ例
"""
表 1.22.3 サンプル 
| 項目A | 項目B  |
|------|--------|
| 値１ | 値あ   |
| 値２ | 値い   |
| 値３ | 値う   |
"""

# 変換結果例
ああああああああああああ
いいいいいいいいい
表 1.22.3 サンプル 
| 項目A | 項目B  |
|------|--------|
| 値１ | 値あ   |
| 値２ | 値い   |
| 値３ | 値う   |
うううううううううう
ええええええええええ


# 依頼本文
{str_honbun}

# テーブルデータ
{str_table}
'''


class Pdf2Text: 
    def __init__(self, llm:AzureChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたはテキストを修正する優秀なアシスタントです。"),
        ("human", message_human  )
        ])

    def run(self, file_pdf,  page_sta, page_end):

        start_time = time.perf_counter()  # 開始時刻

        #tempフォルダの作成
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y%m%d_%H%M%S")
        print(formatted_date)
        file_name_without_ext = os.path.splitext(os.path.basename(file_pdf))[0]  # 拡張子を除いたファイル名
        folder_temp = f'{file_name_without_ext}_{formatted_date}' 
        os.makedirs(folder_temp, exist_ok=True)

        reader = PdfReader(file_pdf)

        for page_number in range(len(reader.pages)):

            # ページ番号の確認
            if page_number + 1  < page_sta :
                print(f"\n--- Skip Page {page_number + 1} ---")
                continue
            if page_number + 1  > page_end + 1:
                print(f"\n--- End Page {page_number + 1} ---")
                break

            # 1ページごとにPDFを分割して保存
            writer = PdfWriter()
            writer.add_page(reader.pages[page_number])  #ここは0から始まるので、page_numberはそのまま使う
            output_1pdf = folder_temp  + '/' + f'output{page_number+1:04d}.pdf'
            with open(output_1pdf, 'wb') as output_file:
                writer.write(output_file)

            output_file = folder_temp  + '/' + f'output{page_number+1:04d}.txt'
            output_file_WT = folder_temp  + '/' + f'output{page_number+1:04d}_WT.txt'

            #1ページのテキストを抽出し保存  本文はpypdfを使う (fitzを使うと項番で１－１－１\n適用のように不要な改行が入る。 PyPDF2はフッターのページ番号が先頭行にきてかつ改行されないので本文とまざる。 ）
            page_text = ""
            reader_1pdf = reader1(output_1pdf)
            for i, page in enumerate(reader_1pdf.pages):
                page_text += page.extract_text()
            with open(output_file, mode='w', encoding='utf-8') as f:
                f.write(page_text) 

            # 1ページのテーブルを抽出し保存  fitzを使ってテーブルを抽出
            doc = fitz.open(output_1pdf)   
            for page_num, page in enumerate(doc):

                # テーブルを検索して抽出
                str_table = ""
                tables = page.find_tables()

                if tables.tables: # テーブルが見つかった場合

                    # テーブルデータを取り出す
                    for i, table in enumerate(tables.tables):
                        s = table.extract()
                        str_table += f"Table {i+1}:" + "\n"
                        str_table += repr(s) + "\n"

                    ##LLMに渡されるプロンプトの確認
                    # formatted_prompt = self.prompt.format_messages(str_honbun=page_text,str_table=str_table)
                    # for message in formatted_prompt:
                    #     print(f"{message.type}: {message.content}")  

                    chain = self.prompt | self.llm | StrOutputParser()
                    print(f"Page {page_number + 1} / {len(reader.pages)}  : テーブル表を整形中・・・ 開始から{time.perf_counter() - start_time :.2f}秒 ")
                    response = chain.invoke({"str_honbun": page_text, "str_table": str_table})   # LLMにテキストを渡して実行  テーブル表テキストの整形
                    honbun_seikei = self.remove_empty_lines_after_table(response)                     # 不要な空行を削除する

                else: # テーブルが見つからなかった場合は、そのままのテキストを使う
                    print(f"Page {page_number + 1}  / {len(reader.pages)}  : テーブル表がないため元のテキストを使います ")
                    honbun_seikei = page_text

                with open(output_file_WT, mode='w', encoding='utf-8') as f:
                    f.write(honbun_seikei) 

            doc.close()  # PDFファイルを閉じる

        return folder_temp

    # テーブル表テキストの整形  不要な空行を削除する
    def remove_empty_lines_after_table(self, text):
        
        lines = text.split("\n")  # 行ごとに分割
        new_lines = []  # 新しい行リストを作成
        
        # 最後の行までループ
        i = 0
        while i < len(lines):
            # "表 "で始まる行が見つかり、その次の行が空行の場合
            if lines[i].startswith("表") and i + 1 < len(lines) and lines[i + 1] == "":
                new_lines.append(lines[i])  # "表 "で始まる行をそのまま追加
                i += 2  # 次の行は空行なのでスキップ
            else:
                new_lines.append(lines[i])  # 通常の行はそのまま追加
                i += 1
        
        # 行を再度結合して結果を返す
        return "\n".join(new_lines)



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

    start_time = time.perf_counter()
    llm = AzureChatOpenAI(  deployment_name=deployment_name, openai_api_version=openai_api_version, openai_api_key=openai_api_key, azure_endpoint=azure_endpoint, temperature=0 )

    pdf2text = Pdf2Text(llm=llm)
    folder_temp = pdf2text.run(file_pdf=r'./doc_raw/kana.pdf', page_sta=7, page_end=21)

    print(folder_temp)

    print(f'end!  開始から{time.perf_counter() - start_time :.2f}秒 ')


