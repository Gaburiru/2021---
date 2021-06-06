import boto3
 
access_key='8FA33F5E68860EEAA159'
secret_key='WzZEQjk5NkZDOUJBNUJEREFCQzAyNkVEMzBGQUEy'
s3 = boto3.resource(
    service_name='s3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url='http://scut.depts.bingosoft.net:29997',
    verify=False
)
BUCKET='zhuolin'
PATH='D:\大数据实训\workspace\文件同步器python版'