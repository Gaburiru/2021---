from tkinter import *
from impala_conn_exec import impala_conn_exec
from element_show import get_database,get_table,get_rows

def display(root):
	root.title("元素区")
	root.geometry('150x500')
	sb = Scrollbar(root)  
	sb.pack(side = RIGHT, fill = Y)  
	  
	mylist = Listbox(root, yscrollcommand = sb.set,height=25)  


	mylist.insert(END, '数据库'+get_database())
	for table in get_table(get_database()):
		mylist.insert(END, '表->'+table)
		if(table!=''):
			for rows in get_rows(table):
				mylist.insert(END, '字段-->'+rows)
	  
	mylist.pack( side = LEFT )  
	sb.config( command = mylist.yview )  
