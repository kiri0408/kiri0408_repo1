
import fitz  # PyMuPDF

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

# 使用例
pdf_file = r"doc_raw\kk.pdf"
page_to_convert = 18  # 変換したいページ番号
output_file = "output" + str(page_to_convert)  +".jpg"


convert_pdf_page_to_jpeg(pdf_file, page_to_convert, output_file, dpi=300)
