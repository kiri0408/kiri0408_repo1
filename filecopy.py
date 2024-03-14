
import glob
import shutil
import os

ori  =r'C:\py\53_ファイルコピー/b'
dist =r'C:\py\53_ファイルコピー\dist'

# 条件に合うファイルパス情報をすべて取得
file_list = glob.glob(  ori + r"/**/*", recursive=True)


for file in file_list:
    if os.path.isfile(file):
        print('コピーします：', file)
        shutil.copy2(file, dist)

print('処理終了')





