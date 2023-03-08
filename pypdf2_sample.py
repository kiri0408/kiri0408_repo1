
"""
https://water2litter.net/rum/post/python_pypdf2_documentinfo/index.html

"""

import PyPDF2
import pandas as pd

df = pd.DataFrame


with open(r'.\pdf\ヤマハ引き落とし明細.pdf', mode='rb') as f:
    reader = PyPDF2.PdfReader(f)
    
    docinfo = reader.metadata
    print('title : ',docinfo.title)   # プロパティを指定する方法
    print('subject : ',docinfo.subject)
    print('作成日',docinfo.creation_date)
    print('更新日 : ', docinfo.modification_date)
    print('author :',docinfo.author)
    print('creator : ', docinfo.creator)
    print('producer : ',docinfo.producer)

    p = reader.pages[0]
    print( float(p.mediabox.width)  * 0.3527 )
    print( float(p.mediabox.height)  * 0.3527 )


