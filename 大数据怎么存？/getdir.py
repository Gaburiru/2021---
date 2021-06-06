import os
from setting import PATH
list_name=[]
def filelist(file_dir=PATH):
	file_list=os.listdir(file_dir)
	for file in file_list:
		if(os.path.isdir(file)):
			filelist(file_dir+'\\'+file)
		else:
			list_name.append(file_dir+'\\'+file)
	return list_name