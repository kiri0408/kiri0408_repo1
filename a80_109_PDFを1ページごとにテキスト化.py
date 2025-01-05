
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
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import time
import re
import random
from pydantic import BaseModel, Field
import glob


class Pdf2Text: 
    def __init__(self, llm:AzureChatOpenAI):
        self.llm = llm


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
            if page_number + 1  > page_sta + 30 :   # 最初のNページでヘッダーフッター見出しを判定する 
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

        return folder_temp




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


