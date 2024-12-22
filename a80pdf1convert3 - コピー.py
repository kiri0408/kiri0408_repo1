# 2 リファクタリング
# 3 画像からの表抽出で使用可能文字を設定
# 100ページで 2.2ドル ３００円ちょっと  １ページ３円

import PyPDF2       # PDFの1ページを切り出し
import pdfplumber   # PDFをテキストに変換
import fitz         # PyMuPDF  PDFを画像に変換
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import base64
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
import time
import traceback
# 処理開始時刻を記録
start_time = time.perf_counter()

# 変数定義

model = ChatOpenAI(model="gpt-4o", temperature=0)

# PDFから１ページのPDFを取り出して保存
def extract_page(input_pdf, output_pdf, page_number):
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        
        if 1 <= page_number <= len(reader.pages):
            writer.add_page(reader.pages[page_number - 1])
            
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            print(f"ページ {page_number} を {output_pdf} として保存しました。")
        else:
            print("指定されたページ番号が範囲外です。")

# PDFを画像へ変換
def convert_pdf_page_to_jpeg(pdf_path, page_number, output_path, dpi=300):
    # PDFファイルを開く
    doc = fitz.open(pdf_path)
    
    # 指定されたページを取得
    page = doc.load_page(page_number - 1)  # ページ番号は0から始まるため、1を引く
    
    # 指定されたDPIでページを画像に変換
    pix = page.get_pixmap(dpi=dpi)
    
    # JPEGとして保存
    pix.save(output_path)
    
    # PDFファイルを閉じる
    doc.close()

# テーブル表テキストの整形  不要な空行を削除する
def remove_empty_lines_after_table(text):
    # 行ごとに分割
    lines = text.split("\n")
    
    # 新しい行リストを作成
    new_lines = []
    
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

# 画像からLLMで表を取り出すときのプロンプト
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "user",
            [
                {"type": "text", "text": (
"""
# 目的   : 画像からテーブル表を抽出
# 命令文 : この画像にテーブル表が含まれる場合、その内容を読み取って以下の例のように、表タイトルと表をセットで出力してください。
           出力する文字は、以下の「使用可能文字」の中から最も近いものを選択してください。  
           表の列がずれないように注意してください。
# 出力形式：テキスト 
# 例 ：
表 1.1.3 電気方式による特性
| 電気方式   |   電圧  |
|------------|---------|
| 三相3 線式 | 15.2V   |
| 三相4 線式 | 14.8V   |
| 単相2 線式 | 10.2V   |

# 使用可能文字：
{str_d}
"""

                )},
                
                {"type": "image_url", "image_url": {"url": "{image_url}"}},
            ],
        ),
    ]
)




class HonbunWT(BaseModel):
    honbun: str = Field(..., description="テーブル表を整えた本文")

class HonbunWTGenerator:
    def __init__(self, llm: ChatOpenAI, ):
        self.llm = llm.with_structured_output(HonbunWT)


    def run(self, str1a: str, str2a: str) -> HonbunWT:
        # プロンプトテンプレートを定義
        prompt_yoyaku = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたは本文中の崩れたテーブル表をきれいに整形する専門家です。",
                ),
                (
                    "human",
'''\

# 目的：依頼本文中の崩れたテーブル表の部分をきれいに整形する。
# 命令文： 崩れたテーブル表の部分を 依頼テーブル調整済みデータ で置き換えた、依頼本文の中身（"""でくくられた中身）を出力してください。 
# 補足 : 例として、本文例 を テーブル調整済みデータ例 で置き換えた結果を 変換結果例 に示しています。 
# 出力形式：テキスト 

# テーブル調整済みデータ例
"""
表 1.22.3 サンプル 
| 項目A | 項目B  |
|------|--------|
| 値１ | 値あ   |
| 値２ | 値い   |
| 値３ | 値う   |
"""

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

# 変換結果例
"""
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
"""

{str_d}
''',
                ),
            ]
        )

        # プロンプトに挿入する対象データを作成する。
        str_c = '''
# 依頼テーブル調整済みデータ
"""
str1b
"""

# 依頼本文
"""
str2b
"""
        '''
        str_c = str_c.replace('str1b',str1a)
        str_c = str_c.replace('str2b',str2a)
        #print(str_c)

        # プロンプト生成を確認するためのコード
        formatted_prompt = prompt_yoyaku.format(str_d=str_c)
        print("Generated Prompt:")
        print(formatted_prompt)


        # ペルソナ生成のためのチェーンを作成
        chain_yoyaku = (
            {"str_d": RunnablePassthrough()}
            | prompt_yoyaku
            | model
            | StrOutputParser()
        )
        # ペルソナを生成
        result = chain_yoyaku.invoke({"str_d": str_c})
        return result if isinstance(result, str) else str(result)
        #return  chain_yoyaku.invoke({"str1": str1, "str2": str2})
        #return chain.invoke({"user_request": user_request})





list_ok=[]
list_ng=[]

for i in range(50,100):

    try:

        int_page = i
        input_pdf = r"doc_raw\kk.pdf" # 入力PDFファイルのパス
        output_pdf = r"doc_raw\output" + str(int_page).zfill(4) + ".pdf"  # 出力PDFファイルのパス  
        output_txt = r"doc_raw\output" + str(int_page).zfill(4) + ".txt"  # 出力txtファイルのパス  
        output_jpg =       r"doc_raw\output" + str(int_page).zfill(4) + ".jpg"  # 出力jpgファイルのパス  
        output_table_txt = r"doc_raw\output" + str(int_page).zfill(4) + "_table.txt"  # 出力jpgファイルのパス  
        output_table_WT  = r"doc_raw\output" + str(int_page).zfill(4) + "_WT.txt"  # 出力jpgファイルのパス  


        # PDFから１ページのPDFを取り出して保存
        extract_page(input_pdf, output_pdf, int_page)


        ######### 該当ページのテキストを抽出 #########
        # PDFファイルを開き、全ページのテキストを抽出し結合する。 基本、１ページしかない。  
        with pdfplumber.open(output_pdf) as pdf:
            str_honbun = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    str_honbun += text + "\n"

        # 抽出したテキストを保存する                                              ★★★★★本文のSTARTとENDのフラグをつけたほうがいい。最後にSTARTとENDの外は強制削除する★★★★★
        with open(output_txt,mode='w', encoding='utf-8') as f:
            f.write(str_honbun) 

        ######### 該当ページからLLMでテーブルのテキストを抽出 #########
        # PDF1ページをJPGへ変換
        convert_pdf_page_to_jpeg(output_pdf, 1, output_jpg, dpi=300)

        print(f'テーブル表を抽出します : {output_jpg}')
        print(f"プログラム処理時間: {time.perf_counter() - start_time :.2f}秒")
        with open( output_jpg , 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            image_url = f'data:image/jpg;base64,{encoded_string}'

        prompt_value = prompt.invoke({  "str_d":str_honbun , "image_url": image_url})
        ai_message = model.invoke(prompt_value)
        str_table = ai_message.content
        str_table = remove_empty_lines_after_table(str_table)  # テーブル表テキストの整形

        with open(output_table_txt, mode='w', encoding='utf-8') as f:
            f.write(str_table) 
        print(str_table)


        ################# 該当ページのテキストのテーブル表の部分をLLMで整形する ################  
        if str_table != 'なし' :   # 該当ページにテーブル表がない場合、なしと出力されているので、その場合は何もしない。
            print(f'本文のテーブル表を成形します : {i}')
            print(f"プログラム処理時間: {time.perf_counter() - start_time :.2f}秒")
            honbunWT_generator = HonbunWTGenerator(llm=model)
            str_honbun_WT = honbunWT_generator.run(str1a=str_table,str2a=str_honbun)
        else:
            str_honbun_WT = str_honbun
        with open(output_table_WT, mode='w', encoding='utf-8') as f:
            f.write(str_honbun_WT) 
        print(str_honbun_WT)

        list_ok.append(str(i))

    except Exception as e:
        list_ng.append(str(i))
        # エラー情報を出力
        print(f"エラーが発生しました: {e}")
        # 詳細なエラー情報を表示
        traceback.print_exc()


print(f'OK = {list_ok}')
print(f'NG = {list_ng}')



print(f"プログラム処理時間: {time.perf_counter() - start_time :.2f}秒")
print('end')

