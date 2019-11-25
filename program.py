# File Objects

import keyword as key


def ignore_tab(X):
	temp = '\t'
	duar = ""
	for i in (len(X)):
		if(((i != (len(X)-1)) and (X[i] != '\'') and (X[i+1] != 't')) or (X[i] == 't')):
			duar = duar + X[i]
	return duar

with open('test.txt', 'r') as f:
	print(f.name)
	f_contents = f.readlines()
	jmlbaris = len(f_contents)
	for i in range (jmlbaris):
		print(f_contents[i])
		
	duar = ignore_tab(f_contents[1])
	print(duar)
	
	print(f_contents)
	#print(key.kwlist)

	#f_contents = [line[:-1] for line in f_contents]
	alist = []
	for i in f_contents:
		alist.append(i.replace('\t',"").replace('\n',''))
	print(f_contents)
	print(alist)
	li = []
	for i in alist:
		li.append(i.replace('\t',"").replace('\n','').split(" "))

	print(key.kwlist)
	print(li)
