# File Objects

import keyword as key


with open('test.txt', 'r') as f:
	print(f.name)
	f_contents = f.readlines()
	print(f_contents)

	print(key.kwlist)
