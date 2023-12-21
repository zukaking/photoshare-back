import decode_img
import boto3
import logging
import sys
import base64
import json
from PIL import Image
from io import BytesIO
import datetime
import uuid
import os
import time

#s3にデータアップロードsagemakerをcallする関数(mikada)
def callsm(img_base64):
    data = img_base64.split(b'base64,')[1]
    data = base64.b64decode(data)
    image = Image.open(BytesIO(data))
    image.save('upImage.jpg')

    client = boto3.client('runtime.sagemaker', 'ap-northeast-1')
    res = client.invoke_endpoint(EndpointName='jumpstart-dft-tf-ic-imagenet-mobilenet-v2-100-224-clas', ContentType='application/x-image',Body=data, Accept='application/json;verbose')
    model_predictions = json.loads(res['Body'].read())
    #predicted_label = model_predictions['predicted_label']
    labels = model_predictions['labels']
    probabilities = model_predictions['probabilities']

    zip_lists = zip(probabilities, labels)
    # 昇順でソート
    zip_sort = sorted(zip_lists,reverse=True)
    # zipを解除
    probabilities, labels = zip(*zip_sort)

    output = {
            #"predicted_label" : predicted_label[0:5],
            "labels" : labels[0:5],
            "probabilities" : probabilities[0:5]
            }
    print(output)
    return  output
key = "test.jpg"
def upload_s3(img_base64,key="test.jpg"):
    
    client = boto3.client('s3',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='ap-northeast-1')
    
    uid = str(uuid.uuid4())
    
    data = img_base64.split(b'base64,')[1]
    data = base64.b64decode(data)
    image = Image.open(BytesIO(data))
    tmpimg = uid + '.jpg'
    image.save(tmpimg)
    
    dt_now = datetime.datetime.now()
       
    bucket = "family-photo-zucca"
    key = dt_now.strftime("%Y-%m-%d-%H-%M-%S_") + uid + ".jpg"
    res = client.upload_file(tmpimg, bucket, key)
    url = f"https://family-photo-zucca.s3.ap-northeast-1.amazonaws.com/{key}"
    
    remove_img(client,key,tmpimg)
    
    return url

def remove_img(client,up_img,local_img):
    upload = False
    start = time.time()
    time_diff = 0     
    while not upload and time_diff < 10:
        res = client.list_objects(Bucket='family-photo-zucca')
        for info in res['Contents']:
            if info['Key'] == up_img:
                os.remove(local_img)
                upload = True
        time.sleep(1)
        end = time.time()
        time_diff = end - start
        
    