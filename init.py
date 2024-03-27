
import os

def init():

    USERPROFILE = os.environ['USERPROFILE']  # 環境変数からユーザフォルダパスを取得 

    print('cps_が無い場合は作成する。')  
    if not os.path.isdir(USERPROFILE + r'\appdata\local\cps_') :
        print('local.tsvを作成します')
        os.mkdir(USERPROFILE + r'\appdata\local\cps_')
        f = open(USERPROFILE + r'\appdata\local\cps_\local.tsv', 'w',encoding='utf-8')
        f.write('path1\t' + r'C:\tmp\test1')
        f.close()
        print('cps_を作成しました')

    print('local.tsvに記載されたpath1を取得する。') 
    with open(USERPROFILE + r'\appdata\local\cps_\local.tsv',encoding='utf-8') as f:
        dic_local = dict(i.rstrip().split('\t', 1) for i in f)  # 右端の改行文字を除去。tabで1回区切る
    path1 = dic_local['path1']

    print('path1のcps.tsvを読み込む')
    with open(path1 + r'\cps.tsv',encoding='utf-8') as f:
        dic_cps = dict(i.rstrip().split('\t', 1) for i in f)  # 右端の改行文字を除去。tabで1回区切る

    print('次回に読み込むサーバ側のフォルダをlocal.tsvに記録')
    with open(USERPROFILE + r'\appdata\local\cps_\local.tsv',encoding='utf-8',mode='w') as f:
        f.write('path1\t' + dic_cps['path1'])

    return dic_cps

dic_cps = init()
print(dic_cps)







