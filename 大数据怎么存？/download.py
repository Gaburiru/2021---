from setting import s3,BUCKET
import botocore
def get_file_by_key(bucket,key):
	try:
		s3.Object(bucket, key).download_file(key)

	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "404":
			print("The object does not exist.")
		else:
			raise
			
import getObject
Objectlist=getObject(BUCKET)
for obj in Objectlist:
	get_file_by_key(BUCKET,obj)
	
		