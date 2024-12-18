"""

4レベルまで分けるようにしたが、文字数が多い場合は、さらに、(\d) のレベルで分けたほうがいい。

"""


import re
import polars as pl
# ファイルからデータを読み込む
with open(r"doc_raw\kk.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 正規表現


pattern1 = r"^第\d+編 .+$"
pattern2 = r"^第\d+章 .+$"
pattern3 = r"^第\d+節 .+$"
pattern4 = r"^\d+\.\d+\.\d+ .+$"

# 各行ごとに正規表現で一致する行を抽出
#matches = [line for line in text.splitlines() if re.match(pattern, line)]

# 結果を出力
#print("\n".join(matches))

i=0
komoku1=''
komoku2=''
komoku3=''
komoku4=''
str_all =[]
content=''
for line  in text.splitlines():
    i+=1
    
    if re.match(pattern1,line):
        str_all.append([i,komoku1,komoku2,komoku3,komoku4,content])
        komoku1=line
        komoku2=''
        komoku3=''
        komoku4=''
        content=''

    elif re.match(pattern2,line):
        str_all.append([i,komoku1,komoku2,komoku3,komoku4,content])
        komoku2=line
        komoku3=''
        komoku4=''
        content=''

    elif re.match(pattern3,line):
        str_all.append([i,komoku1,komoku2,komoku3,komoku4,content])
        komoku3=line
        komoku4=''
        content=''

    elif re.match(pattern4,line):
        str_all.append([i,komoku1,komoku2,komoku3,komoku4,content])
        komoku4=line
        content=''

    else : 
        content+=line

    

print(str_all)

df_all = pl.DataFrame(str_all,strict=False).transpose()
print(df_all)

df_all.write_csv('df_all.tsv',separator='\t')

