import boto3
import logging
from setting import s3
 
def create_bucket(bucket_name):
	s3.create_bucket(Bucket=bucket_name)
