# File Objects

import keyword as key


with open('grammar.txt', 'r') as f:
	"""print(f.name)
	f_contents = f.readlines()
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
	print(li)"""
	f1 = f.read().split("->")
	print(f1)