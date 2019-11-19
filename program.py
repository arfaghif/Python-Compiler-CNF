# File Objects

with open('test.txt', 'r') as f:
	print(f.name)
	f_contents = f.readlines()
	print(f_contents)

