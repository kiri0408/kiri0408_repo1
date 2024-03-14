
import glob
import shutil
import os


print('処理開始')
ori  =r'C:\py\53_ファイルコピー/b'
dist =r'C:\py\53_ファイルコピー\dist'

# 条件に合うファイルパス情報をすべて取得
file_list = glob.glob(  ori + r"/**/*", recursive=True)

i=0
j=0
for file in file_list:
    i+=1
    print(f'{i}/{len(file_list)} ： {file} ')
    if os.path.isfile(file):
        shutil.copy2(file, dist)
        j+=1

print(f'処理終了。  ファイル数は{j}個です。   ')





