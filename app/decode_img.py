import base64
import numpy as np
import io

def decodeBase64(img_base64,image_file):

    #バイナリデータ <- base64でエンコードされたデータ  
    img_binary = base64.b64decode(img_base64)
    with open(image_file,"bw") as f:
        f.write(img_binary)

def encodeBase64(img,b64img):

    file_data = open(img, "rb").read()
    b64_img = base64.b64encode(file_data).decode('utf-8')

    with open(b64img, "w") as f2:
        f2.write(b64_img)