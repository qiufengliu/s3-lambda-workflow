import json
import boto3
from botocore.exceptions import ClientError
import logging
import os
from datetime import datetime
s3 = boto3.client('s3')
state_machine_arn = os.environ['STATE_MACHINE_ARN']
step = 3
step = os.environ['STEP']
stepfunctions = boto3.client('stepfunctions')


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):
    try:
        file_list = []
        response = s3.get_object(
            Bucket=event["Records"][0]["s3"]["bucket"]["name"],
            Key=event["Records"][0]["s3"]["object"]["key"],
        )
        contents=response['Body'].read().decode(encoding="utf-8",errors="ignore")
        for line in contents.splitlines():
            file_list.append(line)
        step = 3
        logger.info(file_list)
        for i in range(0,len(file_list),step):
            batch_input_file = file_list[i:i+step]
            now = datetime.now()
            date_time = now.strftime("%m-%d-%Y-%H-%M-%S-%f")
            run_name = "LambdaJobTrigger-"+date_time
            kwargs = {'stateMachineArn': state_machine_arn, 'name': run_name}
            kwargs['input'] = json.dumps({"FileList":batch_input_file})
            response = stepfunctions.start_execution(**kwargs)
            run_arn = response['executionArn']
            logger.info("Started run %s. ARN is %s.", run_name, run_arn)
            
            
    except ClientError as e:
        logging.error(e)
