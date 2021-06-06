from setting import s3,BUCKET
import botocore
def get_file_by_key(bucket=BUCKET,key):
	try:
		s3.Object(bucket, key).download_file(key)

	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "404":
			print("The object does not exist.")
		else:
			raise
			
def get_big_file(bucket=BUCKET,key):
	try:
		s3resumable=S3Resumable(s3)