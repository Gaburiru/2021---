from input_ui import workspace
from display_ui import display
from result_ui import show_result
from tkinter import *

root1 = Tk()
root2 = Tk()
input=workspace(root1)
display(root2)
root1.mainloop()
root2.mainloop()
