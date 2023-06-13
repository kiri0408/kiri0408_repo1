import os
import datetime
import glob
import shutil

from pathlib import Path

dir_fr_oya = Path(r"C:\py\53_ファイルコピー\a" )  #コピー元の親のフォルダパス
dir_to = r"C:\py\53_ファイルコピー\b"             #コピー先のフォルダパス
types = ['txt','ini']                            #コピー対象の拡張子

#コピー元の親のフォルダパス からコピー元フォルダパスを取得
dir_fr =[]
for path in dir_fr_oya.glob("*"):  
    if path.is_dir():
       dir_fr.append(path) 

#コピー実行 
for dir in dir_fr:  

    for type in types:
        files = glob.glob( str(dir) +  '\*.' + type )

        for file in files:

            if not '- コピー' in file:    #  - コピーを含むファイルは対象外 

                basename = os.path.basename(file)
                time = os.path.getmtime(file)
                datetime1 = datetime.datetime.fromtimestamp(time)
                file_to =  dir_to + '\\' + basename
                print(file)
                shutil.copy2(file, file_to )
