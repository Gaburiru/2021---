from setting import PATH,BUCKET,s3
def delete_object(bucket,key,versionid):
	if(versionid==None):
		versionid=''
	Bucket=s3.Bucket(bucket)
	try:
		response =Bucket.delete_objects(
			Delete={
				'Objects': [
					{
						'Key': key,
						'VersionId': versionid
					},
				],
				'Quiet': True|False
			},
		)
		print("{} delete done".format(key))
	except Exception as e:
		print("upload {} error:{}".format(key, e))

from getObject import objectlist
from getdir import filelist



listpre=filelist()
newlistlocal=[]
for str in listpre:
	s0=str.replace('\\','/')
	s1=s0.replace(PATH.replace('\\','/')+'/','')
	newlistlocal.append(s1)
	
newlists3=[]
for objsum in objectlist():
	newlists3.append(objsum.key)
	
listlocal=sorted(newlistlocal)
lists3=sorted(newlists3)


from getversionbyid import getversionid
if(listlocal!=lists3):
	listtodel=list(set(lists3).difference(set(listlocal)))
	id=[]
	for obj in listtodel:
		id.append(getversionid(BUCKET,obj))
	for iter in listtodel:
		delete_object(BUCKET,iter,id[listtodel.index(iter)])