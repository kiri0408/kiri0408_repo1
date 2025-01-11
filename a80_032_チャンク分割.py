"""
正規表現をもとに、文章の構造を考慮しながらチャンクに分割。  df_all.tsv ファイルを作成する。
100ページで5秒くらい

"""

import re
import polars as pl


class Chunk_bunkatu:
    def __init__(self  ):
        pass


    # コンテンツが長いところは分割する。
    def bunkatu(self,text):

        list_bunkatu=[]
        list_tmp1=[]
        max_mojisu = 500

        if len(text)  > max_mojisu :

            blocks_L1 = re.split(f'(?={self.kajo1})', text, flags=re.MULTILINE)  #箇条書きレベル１で分割してみる。 (?=...) は正の先読みを表します。 この場合、次の文字が...に一致する場合にマッチします。
            for block_L1 in blocks_L1:  #箇条書きレベル１の分割でループ
                print('L1: ' +block_L1)
                print(f'================================={len(block_L1)}================================================')

                if len(block_L1) > max_mojisu :  #箇条書きレベル１の分割でmax_mojisuを超えていた場合

                    if len("".join(list_tmp1)) > 5 :
                        list_bunkatu.append("".join(list_tmp1)) # 分割リストに追加 
                        list_tmp1=[]


                    blocks_L2 = re.split(f'(?={self.kajo2})', block_L1, flags=re.MULTILINE)  #箇条書きレベル１で分割でmax_mojisuを超えていた場合、さらに箇条書きレベル２で分割。   (?=...) は正の先読みを表します。 この場合、次の文字が...に一致する場合にマッチします。
                    for block_L2 in blocks_L2 :
                        print('L2: ' + block_L2) 

                        if len(block_L2) > max_mojisu:  #箇条書きレベル２の分割でmax_mojisuを超えていた場合
                            if len("".join(list_tmp1)) > 5 :
                                list_bunkatu.append("".join(list_tmp1)) # 分割リストに追加 
                                list_tmp1=[]


                            blocks_L3 = re.split(f'(?={self.kajo3})', block_L2, flags=re.MULTILINE)  #箇条書きレベル２で分割でmax_mojisuを超えていた場合、さらに箇条書きレベル３で分割。 (?=...) は正の先読みを表します。 この場合、次の文字が...に一致する場合にマッチします。
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
                    list_tmp1.append(block_L1)
                    if len("".join(list_tmp1)) > max_mojisu:  #最大文字数を超えた場合、
                        list_bunkatu.append("".join(list_tmp1))  # 分割リストに追加 
                        list_tmp1=[]


            if len("".join(list_tmp1)) > 5 :
                list_bunkatu.append("".join(list_tmp1))  # 分割リストに追加 
                list_tmp1=[]


        else:
            list_bunkatu.append(text)

        return list_bunkatu


    def run(self , combined_text, folder_temp ,midashi1, midashi2, midashi3, midashi4, kajo1, kajo2, kajo3) :

        self.text = combined_text
        self.folder_temp = folder_temp
        self.midashi1 = midashi1
        self.midashi2 = midashi2
        self.midashi3 = midashi3
        self.midashi4 = midashi4
        self.kajo1 = kajo1
        self.kajo2 = kajo2
        self.kajo3 = kajo3

        i=0
        komoku1=''
        komoku2=''
        komoku3=''
        komoku4=''
        str_all =[]
        content=''
        for line  in self.text.splitlines():  #テキストを行単位でループ。見出しレベルを考慮してチャンク分割する。
            i+=1
            if re.match(self.midashi1,line)  and not line.strip().endswith("。") :  #見出し1とマッチする場合 (ただし、文末が句点で終わっていない場合)
                str_all.append([i,komoku1,komoku2,komoku3,komoku4,content])
                komoku1=line
                komoku2=''
                komoku3=''
                komoku4=''
                content=''
            elif re.match(self.midashi2,line) and not line.strip().endswith("。") : #見出し2とマッチする場合 (ただし、文末が句点で終わっていない場合)
                str_all.append([i,komoku1,komoku2,komoku3,komoku4,content])
                komoku2=line
                komoku3=''
                komoku4=''
                content=''
            elif re.match(self.midashi3,line) and not line.strip().endswith("。") : #見出し3とマッチする場合 (ただし、文末が句点で終わっていない場合)
                str_all.append([i,komoku1,komoku2,komoku3,komoku4,content])
                komoku3=line
                komoku4=''
                content=''
            elif re.match(self.midashi4,line) and not line.strip().endswith("。") : #見出し4とマッチする場合 (ただし、文末が句点で終わっていない場合)
                str_all.append([i,komoku1,komoku2,komoku3,komoku4,content])
                komoku4=line
                content=''
            else : 
                content = content + line +'\n' 

        str_all.append([i,komoku1,komoku2,komoku3,komoku4,content])  #ver1.1  


        # 見出しでチャンク分割したリストをpolarsのDataFrameに変換
        df_all = pl.DataFrame(str_all, strict=False).transpose()
        df_all = df_all.select(
            pl.col('column_1').alias('midashi1'),
            pl.col('column_2').alias('midashi2'),
            pl.col('column_3').alias('midashi3'),
            pl.col('column_4').alias('midashi4'),
            pl.col('column_5').alias('content'),
        )
        print(df_all)

        # インデックスを作成する （見出しチャンクが大きいときに、箇条書きで分割するためのインデックス）
        df_all = df_all.with_columns(pl.lit(0.0).alias('index') , pl.lit('').alias('delete'))
        for i  in range(len(df_all)):
            df_all[i,'index'] = i 

        for i in range(len(df_all)):
            if i==len(df_all)-10:
                pass
            if len(df_all[i,'content']) > 500:      #見出しチャンクが大きい場合 
                df_all[i,'delete'] = 'del'          #そのチャンクには削除フラグを立てる
                list_bunkatu = self.bunkatu(df_all[i,'content']) #箇条書きで分割する
                #print(list_bunkatu, len(list_bunkatu))  
                for j in range(len(list_bunkatu)):
                    new_row = pl.DataFrame({
                        "midashi1": [df_all[i,'midashi1']], 
                        "midashi2": [df_all[i,'midashi2']], 
                        "midashi3": [df_all[i,'midashi3']], 
                        "midashi4": [df_all[i,'midashi4']], 
                        "content" : [list_bunkatu[j]], 
                        "index"   : [df_all[i,'index'] + (j+1)/100 ],  # 分割したコンテンツは、元のインデックスの枝番的に小数の値を追加することで、元のコンテンツの後ろに並ぶようにする。
                        "delete":['']  
                        }) 
                    df_all = df_all.extend(new_row)  #箇条書きで再分割したものを追加する
                    
        df_all = df_all.sort('index')  #インデックスでソートすることで、大きい見出しチャンクを箇条書きで再分割したものが正しい順番で並ぶようにする。


        # 埋め込み用の 項目データ込みのembedded用コンテンツ、およびメタデータを作成、追加  
        pattern1_emb = self.midashi1.replace('.+$','').replace('^','')    #見出しの部分だけを取り出す
        pattern2_emb = self.midashi2.replace('.+$','').replace('^','')    #見出しの部分だけを取り出す
        pattern3_emb = self.midashi3.replace('.+$','').replace('^','')    #見出しの部分だけを取り出す
        pattern4_emb = self.midashi4.replace('.+$','').replace('^','')    #見出しの部分だけを取り出す
        patterns_emb = [pattern1_emb, pattern2_emb, pattern3_emb, pattern4_emb]
        df_all = df_all.with_columns( ( pl.col('midashi1') + pl.col('midashi2')  + pl.col('midashi3') + pl.col('midashi4') ).alias('emb') )  
        df_all = df_all.with_columns( ( pl.col('midashi1') +' ' + pl.col('midashi2')  +' ' + pl.col('midashi3')  +' '+ pl.col('midashi4') ).alias('meta') )  
        for i in range(len(df_all)):
                # 各パターンを適用して削除
            for pattern in patterns_emb:
                df_all[i,'emb']  = re.sub(pattern, "", df_all[i,'emb'] ) 
            df_all[i,'emb'] += '::\n' 
            df_all[i,'emb'] += df_all[i,'content']

        df_all = df_all.filter(pl.col('delete') != 'del')  #削除フラグが立っているものを削除
        df_all = df_all.sort(pl.col('index'))              #インデックスでソート
        df_all.write_csv(self.folder_temp + r'./df_all.tsv',separator='\t')

        print('df_all.tsvを作成しました。')

        return df_all

######################### 単独実行用main #############################
if __name__ == "__main__":

    #kana
    with open(r'./kana_20250104_154214/combined_text.txt', 'r', encoding='utf-8') as f:
        combined_text = f.read()
    folder_temp ="kana_20250104_154214"
    midashi1 ="^第[０-９\d]+\s*章\s.+$"
    midashi2 ="^第[０-９\d]+\s*節\s.+$"
    midashi3 ="^[０-９\d]+－[０-９\d]+－[０-９\d]+\s.+$"
    midashi4 ="xxxxxxxxxxxxxxxxx"  
    kajo1    ="^\d+"
    kajo2    ="^[ｱ-ﾜ]"
    kajo3    ="^[a-z]"

    #kk
    with open(r'./kk_20250105_101542/combined_text.txt', 'r', encoding='utf-8') as f:
        combined_text = f.read()
    folder_temp ="kk_20250105_101542"
    midashi1=	"^第\s*[０-９\d]+\s*編\s.+$"
    midashi2=	"^第\s*[０-９\d]+\s*章\s.+$"
    midashi3=	"^第\s*[０-９\d]+\s*節\s.+$"
    midashi4=	"^[０-９\d]+\.[０-９\d]+\.[０-９\d]+\s.+$"
    kajo1=	"^\([０-９\d]+\)"
    kajo2=	"^\([ｱ-ﾝ]\)"
    kajo3=	"^\([a-z]\)"

    #kk_kai
    with open(r'./kk_kai_20250104_193658/combined_text.txt', 'r', encoding='utf-8') as f:
        combined_text = f.read()
    folder_temp ="kk_kai_20250104_193658"
    midashi1=	"^第\s*[０-９\d]+\s*編\s.+$"
    midashi2=	"^第\s*[０-９\d]+\s*章\s.+$"
    midashi3=	"^第\s*[０-９\d]+\s*節\s.+$"
    midashi4=	"^[０-９\d]+\.[０-９\d]+\.[０-９\d]+\s.+$"
    kajo1=	"^\([０-９\d]+\)"
    kajo2=	"^\([ｱ-ﾝ]\)"
    kajo3=	"^\([a-z]\)"

    chunk_bunkatu_ = Chunk_bunkatu()
    df_all = chunk_bunkatu_.run(combined_text=combined_text  , folder_temp=folder_temp ,midashi1=midashi1, midashi2=midashi2, midashi3=midashi3, midashi4=midashi4, kajo1=kajo1, kajo2=kajo2, kajo3=kajo3)

    print(df_all)





