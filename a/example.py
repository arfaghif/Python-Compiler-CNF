#usage: pyhton3 example.py

from CYK_Paser import Grammar

g = Grammar('example_grammar1.txt')
"""
with open("input.txt",'r') as file:
    data = file.read()
    g.parse(data)
    #g.printParseTab()
    """
with open("input1.txt",'r') as file:
    data = file.read()
    g.parse(data)
    
    #g.printParseTab()
    """
with open("input2.txt",'r') as file:
    data = file.read()
    g.parse(data)
    #g.printParseTab()

with open("input3.txt",'r') as file:
    data = file.read()
    g.parse(data)
    #g.printParseTab()
"""
file = open("input1.txt")
i =1
for line in  file :
    print("HASIL BARIS KE" ,i)
    if (line == "") :
        print("ACCEPTED")
    else :
        g.parse(line)
        if (i==4) :
            pass
            #g.printParseTab()
    i += 1



"""g.parse("from PIL import Image")
g.print_parse_table()"""

print('')
print('')
print('')
"""
g = Grammar('example_grammar2.txt')
g.parse(' 2')
#g.print_parse_table()

print('')
print('')
print('')

g = Grammar('example_grammar2.txt')
g.parse('eats she fork a fish')
g.print_parse_table()
#g.get_trees()
"""

