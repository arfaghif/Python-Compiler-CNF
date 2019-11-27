#usage: pyhton3 example.py

from CYK_Paser import Grammar

g = Grammar('example_grammar1.txt')

file = open("input3.txt")
i =1
for line in  file :
    print("HASIL BARIS KE" ,i)
    if (line == "") :
        print("ACCEPTED")
    else :
        g.parse(line)
        if (i==14) :
            g.printParseTab()
            pass
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

