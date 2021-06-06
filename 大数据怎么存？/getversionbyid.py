from setting import s3,BUCKET

def getversionid(bucket,key):
	object=s3.Object(bucket,key)
	return object.version_id