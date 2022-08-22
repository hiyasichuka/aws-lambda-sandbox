import os
import boto3
import urllib.parse
from io import BytesIO
from PIL import Image, ImageFilter

TARGET_BUCKET_NAME = os.environ.get('TARGET_BUCKET_NAME')


def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Putされたバケット名やキーを取得
    origin_bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    # 画像をGet
    response = s3.get_object(Bucket=origin_bucket_name, Key=key)

    # 圧縮
    im = Image.open(response['Body'])
    im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=50, progressive=True)

    # 画像をPut
    s3.put_object(Body=im_io.getvalue(),
                  Bucket=TARGET_BUCKET_NAME, Key=key)

    return None
