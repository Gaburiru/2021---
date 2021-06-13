
# 导入连接工具
from impala.dbapi import connect
# 导入as_pandas工具，可以将获取到的数据转化为 dataframe或者 Series
from impala.util import as_pandas
#登入设置
host='bigdata129.depts.bingosoft.net'
port=22129
user='user34'
password='pass@bingo34'
database='user34_db'

def impala_conn_exec(sql):
# 得到连接，
	conn = connect(host=host, port=port, auth_mechanism='PLAIN', user=user,password=password,  database=database)
# 得到句柄
	cursor = conn.cursor()
# 执行查询
	cursor.execute(sql)
# 结果
	data_list=cursor.fetchall()
	return data_list