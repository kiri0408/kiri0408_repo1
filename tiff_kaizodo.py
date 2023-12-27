from PIL import Image

# TIFF画像の読み込み
image_path = "./image_file/a.tif"
image = Image.open(image_path)

# 新しい値でタグを更新
image.tag[256] = (555,)  # 幅
image.tag[257] = (444,)  # 高さ
# 他のタグも同様に更新可能

print(image.info)
print(image.info["dpi"]) # DPIを取得する

# 更新を適用して画像を保存
updated_image_path = "./image_file/aa.tif"
image.save(updated_image_path, dpi=(150,150))


import numpy as np
import cv2

import sys, os
from PIL import Image
img_pil = Image.open(image_path)
FITC = []

try:
    count = 0
    while count<=5:
        img_pil.seek(count)
        img = np.asarray(img_pil)
        #img.flags.writeable = True
        #img = cv2.resize(img,(512,512))
        FITC.append(img)
        count += 1
        print(count,end=",")
except EOFError:
    pass

FITC = np.array(FITC)
print(FITC.shape)


stack = []
for img in FITC:
    stack.append(Image.fromarray(img))
stack[0].save('./aaa.tif', compression="tiff_deflate", save_all=True, append_images=stack[1:],dpi=(44,44))


