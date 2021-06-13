from tkinter import *
from result_ui import show_result

def workspace(root):
	root.title("工作区")
	root.geometry('600x480')
	v = StringVar()
	e = Entry(root,textvariable=v,width=300)
	e.pack()

	def submit():
		input = e.get()
		root3=Tk()
		show_result(root3,input)
		root3.mainloop()
		
	b = Button(root,text="submit",width=15,height=2,command=submit)
	b.pack()
