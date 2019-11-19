# File Objects

import keyword as key


def ignore_tab(X):
	temp = '\t'
	duar = ""
	for i in (X):
		if((i != '\') and (i+1 != 't')):
			duar = duar + i
	return duar

with open('test.txt', 'r') as f:
	print(f.name)
	f_contents = f.readlines()
	jmlbaris = len(f_contents)
	for i in range (jmlbaris):
		print(f_contents[i])
		
	print(f_contents)
	#print(key.kwlist)
