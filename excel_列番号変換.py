def toAlpha2(num):
    i = int((num-1)/26)
    j = int(num-(i*26))
    Alpha = ''
    for z in i,j:
        if z != 0:
            Alpha += chr(z+64)
    return Alpha

import re
import sys
def convert_alphabet2num(alphabet):
    """アルファベットと数字に変換します。「AB」なら「28」に変換します。"""
    if not re.search(r"\A[A-Z]+\Z", alphabet):
        sys.exit("ERROR: '{}' is invalid value".format(alphabet))
    num = 0
    for cnt, val in enumerate(list(alphabet)):
        num += pow(26, len(alphabet) - cnt - 1)*(ord(val) - ord('A') + 1)
    return num


#print(toAlpha2(7))
print(convert_alphabet2num('A'))
print(convert_alphabet2num('Z'))
print(convert_alphabet2num('AA'))
print(convert_alphabet2num('AZ'))

