#usage: pyhton3 example.py

from CYK_Paser import Grammar

g = Grammar('example_grammar1.txt')
g.parse("for dscsdc in range (5):")
g.print_parse_table()

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

