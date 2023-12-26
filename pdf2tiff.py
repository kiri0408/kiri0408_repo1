"""

指定したフォルダ内のPDFファイルをTIFFへ変換する。

poppler-windows
https://github.com/oschwartz10612/poppler-windows/releases

"""

import os
from pathlib import Path
from pdf2image import convert_from_path
import glob
import os

# poppler/binを環境変数PATHに追加する
poppler_dir = Path(__file__).parent.absolute() / r"C:\Users\arwml\~tools\poppler-23.11.0\Library\bin"
os.environ["PATH"] += os.pathsep + str(poppler_dir)

# 出力先のtiffフォルダ
image_dir = Path("./image_file")

# 変換元PDFフォルダから ファイル名の一覧を取得 
pdf_fol = r"C:\py\64_pdf_tiff変換\pdf_file\*.pdf"
pdf_paths = glob.glob(pdf_fol)

# 元のPDFファイルごとにtiff変換し保存していく 
i=0
for pdf_path in pdf_paths:

    i+=1
    print(  f' {i}  /  {len(pdf_paths)}  :  {pdf_path}    '  )

    # PDF -> Image に変換
    pages = convert_from_path(str(pdf_path), 400)  # dpiの数値を指定

    filename = os.path.splitext(os.path.basename(pdf_path))[0]  #ファイル名(拡張子なし)の取り出し
    tiff_name = filename + ".tif"
    image_path = image_dir / tiff_name 
    pages[0].save(str(image_path), "TIFF", compression="tiff_deflate", save_all=True, append_images=pages[1:]) # tiffファイルとして保存。 データロスのない圧縮方式（"tiff_deflate"）を指定

