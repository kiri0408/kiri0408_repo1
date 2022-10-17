
data=()
data2=[]
for i in range(1000000):
    ord = 'F' + str(i)
    data = ( ord ,'kotei1' ,'2022-06-01 00:00:00.000' , i%10 )
    data2.append(data)

import csv

with open('out.tsv', mode='w', newline='', encoding='utf-8') as fo:
    tsv_writer = csv.writer(fo, delimiter='\t')
    tsv_writer.writerows(data2)