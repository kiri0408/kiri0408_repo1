
import os
import datetime
import pandas as pd

dir_path = "C:\pyenv" 
max_file = 10000  #検索する最大ファイル数 

df = pd.DataFrame(columns=['path','size','date'])

i=0
for current_dir, sub_dirs, files_list in os.walk(dir_path): 
  for file_name in files_list: 
    file_path = os.path.join(current_dir,file_name)
    file_size = os.path.getsize(file_path)
    ts = os.path.getmtime(file_path)
    d = datetime.datetime.fromtimestamp(ts)
    s = d.strftime('%Y-%m-%d')
    print(i,file_path,file_size,s)
    df.loc[i,'path'] = file_path
    df.loc[i,'size'] = file_size
    df.loc[i,'date'] = s
    i+=1
    if i == max_file:
      break
  if i == max_file:
    break

df.to_csv('df.tsv', sep='\t')


