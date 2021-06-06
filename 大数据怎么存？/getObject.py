from setting import s3,BUCKET


def objectlist(bucket=BUCKET):
	Object=[]
	Bucket=s3.Bucket(bucket)
	for object in Bucket.objects.all():
		Object.append(object)
	
	return Object
	