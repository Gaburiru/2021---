from impala_conn_exec import impala_conn_exec
from tkinter import *
import pandas as pd

def show_result(root,input):
	if(input!=''):
		try:
			result=impala_conn_exec(input)
		except Exception as e:
			result=e
	else:
		result=''
		
	root.title("结果区")
	sb = Scrollbar(root)  
	sb.pack(side = RIGHT, fill = Y)
	sb2 = Scrollbar(root)  
	sb2.pack(side=BOTTOM,fill=X)
	text = Text(root)
	text.pack()
	text.insert("insert", result)
