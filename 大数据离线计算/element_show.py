from impala_conn_exec import impala_conn_exec,database
def get_database():
	"""
	result=impala_conn_exec('show databases')
	list=[]
	for database in result:
		list.append(str(database[0]))
	return list
	"""
	return database
	
def get_table(database_name):
	result=impala_conn_exec('show tables from '+database_name)
	list=[]
	for table in result:
		list.append(str(table[0]))
	return list
	
def get_rows(table_name):
	result=impala_conn_exec('show columns FROM '+ table_name)
	list=[]
	for rows in result:
		list.append(str(rows[0]))
	return list
