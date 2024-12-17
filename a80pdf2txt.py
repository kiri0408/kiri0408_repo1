import pdfplumber

# PDFファイルのパスを指定
pdf_path = r"doc_raw\kk_kai.pdf"

i=0
# PDFファイルを開く
with pdfplumber.open(pdf_path) as pdf:
    # 全ページのテキストを結合する
    all_text = ""
    for page in pdf.pages:
        i+=1
        print(i)
        text = page.extract_text()
        if text:
            all_text += text + "\n"

with open(r"doc_raw\kk_kai.txt",mode='w', encoding='utf-8') as f:
    f.write(all_text) 

# 抽出されたテキストを表示
print(all_text)

