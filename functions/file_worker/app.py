import json
import boto3
from botocore.exceptions import ClientError
import re
import logging
s3 = boto3.client('s3')
s3_path_pattern = re.compile("^s3://([^/]+)/(.*?([^/]+))$")

def lambda_handler(event, context):
    try:
        file_list = event["FileList"]
        file_meta = []
        total_size = 0
        tmp_file = open('/tmp/tmp_file.csv', 'w')
        result_key = ''
        for f in file_list:
            result = s3_path_pattern.match(f)
            if s3_path_pattern.match(f):
                bucket_name= result.group(1)
                object_key = result.group(2)
                response = s3.get_object(Bucket=bucket_name,Key=object_key)
                ######
                # csv file processing sample 
                contents=response['Body'].read().decode(encoding="utf-8",errors="ignore")
                tmp_file.writelines(contents)
                ######
                size = response["ContentLength"]
                total_size = total_size + size
                result_key = result_key + object_key
                file_meta.append({"bucket_name":bucket_name,"object_key":object_key,"size":size})

        tmp_file.close()
    except ClientError as e:
        logging.error(e)

    # result upload  
    try:
        response = s3.upload_file('/tmp/tmp_file.csv', bucket_name, result_key)
    except ClientError as e:
        logging.error(e)

    return {
        "file_meta": file_meta,
        "result_key": result_key,
        "total_size":str(total_size)
    }