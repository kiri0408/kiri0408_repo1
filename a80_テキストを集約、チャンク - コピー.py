import re

fol_text =r'doc_raw\kk_data1\\'

page_start=1
page_end=100


# 操作を実行する関数
def modify_text(input_text):
    # 文字列を行ごとに分割
    lines = input_text.splitlines()

    # 削除開始と終了のフラグ
    start_index = None
    end_index = None

    # pattern_headder = r"^公共建築改修工事標準仕様書"  # kk_kaiの場合
    pattern_headder = r"^公共建築工事標準仕様書"  # kkの場合
    pattern_footer = r"^\d+ 国土交通省大臣官房官庁営繕部"

    # 各行を走査
    for i, line in enumerate(lines):
        if re.match(pattern_headder, line):
            start_index = i
        if re.match(pattern_footer, line):
            end_index = i

    # 該当範囲を削除
    if start_index is not None and end_index is not None:
        lines = lines[start_index + 1 : end_index]  # 範囲外の部分を残す

    # 結果を結合して返す
    return "\n".join(lines) +'\n',start_index ,end_index

str_text = ''
for int_page in range(page_start,page_end):  

    filename = 'output' + str(int_page).zfill(4) + '_WT.txt'
    input_file = fol_text + filename
    print(input_file)
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # 実行
    result ,start_index ,end_index= modify_text(text)   # PDFの各ページのヘッダ、フッタを削除する  

    print(result)
    str_text += result 

# 結果の出力
print(str_text)
output_txt =r'doc_raw\shuyaku.txt'
with open(output_txt,mode='w', encoding='utf-8') as f:
    f.write(str_text) 

import re
import polars as pl
# ファイルからデータを読み込む
#with open(r"doc_raw\kk.txt", "r", encoding="utf-8") as file:
#    text = file.read()

text = str_text

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
        content = content + line +'\n' 


str_all.append([3924 + 0.1 , komoku1,komoku2,komoku3,komoku4,content])

print(str_all)


df_all = pl.DataFrame(str_all, strict=False).transpose()

df_all = df_all.select(
    pl.col('column_1').alias('midashi1'),
    pl.col('column_2').alias('midashi2'),
    pl.col('column_3').alias('midashi3'),
    pl.col('column_4').alias('midashi4'),
    pl.col('column_5').alias('content'),
)


# インデックスを作成する
df_all = df_all.with_columns(pl.lit(0.0).alias('index') , pl.lit('').alias('delete'))
for i  in range(len(df_all)):
    df_all[i,'index'] = i 


# コンテンツが長いところは分割する。

def bunkatu(text):

    list_bunkatu=[]
    list_tmp1=[]
    max_mojisu = 500

    if len(text)  > max_mojisu :

        blocks = re.split(r"(?=^\(\d+\))", text, flags=re.MULTILINE)
        for block in blocks:
            print('L1: ' +block)
            print(f'================================={len(block)}================================================')

            if len(block) > max_mojisu :

                if len("".join(list_tmp1)) > 5 :
                    list_bunkatu.append("".join(list_tmp1)) # 分割リストに追加 
                    list_tmp1=[]


                blocks_L2 = re.split(r"(?=^\([ｱ-ﾜ]\))", block, flags=re.MULTILINE)
                for block_L2 in blocks_L2 :
                    print('L2: ' + block_L2) 

                    if len(block_L2) > max_mojisu:
                        if len("".join(list_tmp1)) > 5 :
                            list_bunkatu.append("".join(list_tmp1)) # 分割リストに追加 
                            list_tmp1=[]


                        blocks_L3 = re.split(r"(?=^\([a-z]\))", block_L2, flags=re.MULTILINE)
                        for block_L3 in blocks_L3:
                            print('L3: ' + block_L3)
                            
                            list_tmp1.append(block_L3)
                            if len("".join(list_tmp1)) > max_mojisu:  #最大文字数を超えた場合、
                                list_bunkatu.append("".join(list_tmp1))  # 分割リストに追加 
                                list_tmp1=[]


                    else:
                        list_tmp1.append(block_L2)
                        if len("".join(list_tmp1)) > max_mojisu:  #最大文字数を超えた場合、
                            list_bunkatu.append("".join(list_tmp1))  # 分割リストに追加 
                            list_tmp1=[]

                if len("".join(list_tmp1)) > 5 :
                    list_bunkatu.append("".join(list_tmp1))  # 分割リストに追加 
                    list_tmp1=[]



            else:
                list_tmp1.append(block)
                if len("".join(list_tmp1)) > max_mojisu:  #最大文字数を超えた場合、
                    list_bunkatu.append("".join(list_tmp1))  # 分割リストに追加 
                    list_tmp1=[]


        if len("".join(list_tmp1)) > 5 :
            list_bunkatu.append("".join(list_tmp1))  # 分割リストに追加 
            list_tmp1=[]


    else:
        list_bunkatu.append(text)

    return list_bunkatu

for i in range(len(df_all)):
    if len(df_all[i,'content']) > 500:
        df_all[i,'delete'] = 'del'
        list_bunkatu = bunkatu(df_all[i,'content'])
        print(list_bunkatu, len(list_bunkatu))
        for j in range(len(list_bunkatu)):
            new_row = pl.DataFrame({
                "midashi1": [df_all[i,'midashi1']], 
                "midashi2": [df_all[i,'midashi2']], 
                "midashi3": [df_all[i,'midashi3']], 
                "midashi4": [df_all[i,'midashi4']], 
                "content" : [list_bunkatu[j]], 
                "index"   : [df_all[i,'index'] + (j+1)/100 ],  # 分割したコンテンツは、元のインデックスの枝番的に小数の値を追加する
                "delete":['']  
                }) 
            print(new_row)
            print(new_row[0,'content'])
            #df_all = df_all.extend(new_row).sort('index')
            df_all = df_all.extend(new_row)
            pass
df_all = df_all.sort('index')


# 埋め込み用の 項目データ込みのembedded用コンテンツ、およびメタデータを作成、追加  
pattern1_emb = r"第\d+編"
pattern2_emb = r"第\d+章"
pattern3_emb = r"第\d+節"
pattern4_emb = r"\d+\.\d+\.\d+"
patterns_emb = [pattern1_emb, pattern2_emb, pattern3_emb, pattern4_emb]
df_all = df_all.with_columns( ( pl.col('midashi1') + pl.col('midashi2')  + pl.col('midashi3') + pl.col('midashi4') ).alias('emb') )  
df_all = df_all.with_columns( ( pl.col('midashi1') +' ' + pl.col('midashi2')  +' ' + pl.col('midashi3')  +' '+ pl.col('midashi4') ).alias('meta') )  
for i in range(len(df_all)):
        # 各パターンを適用して削除
    for pattern in patterns_emb:
        df_all[i,'emb']  = re.sub(pattern, "", df_all[i,'emb'] ) 
    df_all[i,'emb'] += '::\n' 
    df_all[i,'emb'] += df_all[i,'content']



print(df_all)
df_all = df_all.sort(pl.col('index'))
df_all.write_csv(r'doc_raw\df_all.tsv',separator='\t')
print(df_all.columns,df_all.dtypes)

