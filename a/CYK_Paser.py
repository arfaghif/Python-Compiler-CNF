### Author
'''
Iker García Ferrero
Github: https://github.com/ikergarcia1996
'''
# Example Of Use
 
'''
# Initialize the grammar and read the rules from a file
g = Grammar('example_grammar1.txt')

# Parse a sentence
g.parse('astronomers saw stars with ears')

# Print the table used for parsing the sentence
g.print_parse_table()

# Get the list of trees generated for the sentence
trees = g.get_trees()

# Get the result of the production rule, VP, S, NP... 
p = trees[0].get_type

# Get the left child of the production rule
l = trees[0].get_left

# Get the right child of the production rule
d = trees[0].get_right
'''

 ## Expected output

 
'''
Grammar file readed succesfully. Rules readed:
S --> NP VP
PP --> P NP
VP --> V NP
VP --> VP PP
NP --> NP PP
NP --> astronomers
NP --> ears
NP --> saw
V --> saw
NP --> telescope
NP --> stars
P --> with

Applied Rule: VP[2,2] --> V[1,2] NP[1,3]
Applied Rule: PP[2,4] --> P[1,4] NP[1,5]
Applied Rule: S[3,1] --> NP[1,1] VP[2,2]
Applied Rule: NP[3,3] --> NP[1,3] PP[2,4]
Applied Rule: VP[4,2] --> V[1,2] NP[3,3]
Applied Rule: VP[4,2] --> VP[2,2] PP[2,4]
Applied Rule: S[5,1] --> NP[1,1] VP[4,2]
Applied Rule: S[5,1] --> NP[1,1] VP[4,2]
----------------------------------------
The sentence IS accepted in the language
Number of possible trees: 2
----------------------------------------

-----------  ------------  ------  ------  ------
['S', 'S']
[]           ['VP', 'VP']
['S']        []            ['NP']
[]           ['VP']        []      ['PP']
['NP']       ['NP', 'V']   ['NP']  ['P']   ['NP']
astronomers  saw           stars   with    ears
-----------  ------------  ------  ------  ------
'''


# Example of grammar file
'''
S -> NP VP
PP -> P NP
VP -> V NP
VP -> VP PP
NP-> NP PP
NP -> astronomers
NP -> ears
NP -> saw
NP-> telescope
NP -> stars
P -> with
V -> saw
'''

import keyword

class Dictlist(dict):
    
    def __setitem__(self, key, value):
        
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)


class production_rule(object):
    
    result = None
    p1 = None
    p2 = None
    
    #Parameters:
    #   Result: String
    #   p1: Production rule (left child of the production rule)
    #   p2: Production rule (right child of the production rule)
    def __init__(self,result,p1,p2):
        self.result = result
        self.p1 = p1
        self.p2 = p2
    
    #Returns the result of the production rule, VP, S, NP... 
    @property
    def get_type(self):
        return self.result
    
    #Returns the left child of the production rule
    @property
    def get_left(self):
        return self.p1
    
    #Returns the right child of the production rule
    @property
    def get_right(self):
        return self.p2

class Cell(object):
    productions = []
    
    
    #Parameters:
    #   Productions: List of production rules
    
    def __init__(self, productions=None):
        if productions is None:
            self.productions = []
        else:
            self.productions = productions
            
    def add_production(self, result,p1,p2):
        self.productions.append(production_rule(result,p1,p2))
    
    def set_productions(self, p):
        self.productions = p
    
    @property
    def get_types(self):
        types = []
        for p in self.productions:
            types.append(p.result)
        return types
    @property
    def get_rules(self):       
        return self.productions


class Grammar(object):
    
    grammar_rules = Dictlist()
    parse_table = None
    length = 0
    tokens = []
    number_of_trees = 0
    start = []
    
    #Parameters:
    #   Filename: file containing a grammar
    
    def __init__(self, filename):
        self.grammar_rules = Dictlist()
        self.parse_table = None
        self.length = 0
        self.start = []
        file = open(filename)
        for line in file:
            if (line[0] == "#" or line[0] == "\n"):
                continue
            if (line[0] == "$" ):
                self.start.append(line.split("->")[1].rstrip().strip())
                continue
            a, b = line.split("->")
            self.grammar_rules[b.rstrip().strip()]=a.rstrip().strip()
        
        if len(self.grammar_rules) == 0:
            raise ValueError("No rules found in the grammar file")
        print('')
        print('Grammar file readed succesfully. Rules readed:')
        self.print_rules()
        print('')
        
    #Print the production rules in the grammar
    def print_rules(self):
        pass
    """
    def print_rules(self):
        for r in self.grammar_rules:
            for p in self.grammar_rules[r]:
                print(str(p) + ' --> ' + str(r))
        """
    def apply_rules(self,t):
        try:
            #print(self.grammar_rules[t])
            return self.grammar_rules[t]
        except KeyError as r:
            return None
            
    #Parse a sentence (string) with the CYK algorithm   
    def parse(self,sentence):
        self.number_of_trees = 0
        self.tokens = lexer(sentence.replace("True", "1").replace("False", "1").replace("None", "1"))
        self.length = len(self.tokens)
        if self.length < 1:
            raise ValueError("The sentence could no be read")
        self.parse_table = [ [Cell() for x in range(self.length - y)] for y in range(self.length) ]
        
         #Process the first line
        for x, t in enumerate(self.tokens):
            r = self.apply_rules(t)
            self.parse_table[0][x].add_production("MAny",production_rule(t,None,None),None)
            if len(t.split())==1 :
                self.parse_table[0][x].add_production("Any",production_rule(t,None,None),None)
            if isVar(t) :
                self.parse_table[0][x].add_production("Var",production_rule(t,None,None),None)
            if isInt(t):
                self.parse_table[0][x].add_production("Int",production_rule(t,None,None),None)
                self.parse_table[0][x].add_production("Bool",production_rule(t,None,None),None)
            if r != None:
                for w in r: 
                    self.parse_table[0][x].add_production(w,production_rule(t,None,None),None)
        
        
        #Run CYK-Parser
        
        
        for l in range(2,self.length+1):
            for s in range(1,self.length-l+2):
                self.parse_table[l-1][s-1].add_production("MAny",None,None)
                for p in range(1,l-1+1):
                    t1 = self.parse_table[p-1][s-1].get_rules
                    t2 = self.parse_table[l-p-1][s+p-1].get_rules
                            
                    for a in t1:
                        for b in t2:
                            #print(a,b,r)
                            r = self.apply_rules(str(a.get_type) + " " + str(b.get_type))
                            if r is not None:
                                for w in r:
                                    #print('Applied Rule: ' + str(w) + '[' + str(l) + ',' + str(s) + ']' + ' --> ' + str(a.get_type) + '[' + str(p) + ',' + str(s) + ']' + ' ' + str(b.get_type)+ '[' + str(l-p) + ',' + str(s+p) + ']')
                                    self.parse_table[l-1][s-1].add_production(w,a,b)
                               
        self.number_of_trees = len(self.parse_table[self.length-1][0].get_types)
        if   (isanysame(self.parse_table[self.length-1][0].get_types,self.start)) :
            print("----------------------------------------")
            print('The sentence IS accepted in the language')
            print('Number of possible trees: ' + str(self.number_of_trees))
            print("----------------------------------------")
            
        else:
            print("--------------------------------------------")
            print('The sentence IS NOT accepted in the language')
            print("--------------------------------------------")
        
        
    #Returns a list containing the parent of the possible trees that we can generate for the last sentence that have been parsed
    def get_trees(self):
        return self.parse_table[self.length-1][0].productions
                
                
    #@TODO
    def print_trees(self):
        pass
                      
    #Print the CYK parse trable for the last sentence that have been parsed.             
    def print_parse_table(self):
        
        
        try:
            from tabulate import tabulate
        except (ModuleNotFoundError,ImportError) as r:
            import subprocess
            import sys
            import logging
            logging.warning('To print the CYK parser table the Tabulate module is necessary, trying to install it...')
            subprocess.call([sys.executable, "-m", "pip", "install", 'tabulate'])

            try:
                from tabulate import tabulate
                logging.warning('The tabulate module has been instaled succesfuly!')

            except (ModuleNotFoundError,ImportError) as r:
                logging.warning('Unable to install the tabulate module, please run the command \'pip install tabulate\' in a command line')

        
        lines = [] 
        
        
        
        for row in reversed(self.parse_table):
            l = []
            for cell in row:
                l.append(cell.get_types)
            lines.append(l)
        
        lines.append(self.tokens)
        print('')
        print(tabulate(lines))
        print('')
    
def isanysame(L1, L2):
    for i in L1:
        if i in L2:
            return True
    return False

def isVar(r):
    if r not in keyword.kwlist :
        if ((ord(r[0]) in range (65, 91)) or (ord(r[0]) in range (97, 123)) or (ord(r[0])==95)) :
            for i in r :
                if not (((ord(r[0]) in range (65, 91)) or (ord(r[0]) in range (97, 123)) or (ord(r[0])==95) or (ord(r[0]) in range (48, 58)))) :
                    return False
            return True
    return False

def isInt(t):
    for i in t :
        if not(ord(i) in range (48,58)):
            return False
    return True


def lexer(string):
    symbols = ['(', ')', '[', ']', ">", "<", "!", '"', '*',"/", "+", "-","%", ':', ',',"'", '='] # single-char keywords
    KEYWORDS =keyword.kwlist
    KEYWORDS.append("range")
    skip = ["\n","","\t"]
    valid = [ "A" , "B" , "C" , "D" , "E" , "F" , "G" , "H" , "I" , "J" , "K" , "L" , "M" , "N" , "O" , "P" , "Q" , "R" , "S" , "T" , "U" , "V" , "W" , "X" , "Y" , "Z" , "a" , "b" , "c" , "d" , "e" , "f" , "g" , "h" , "i" , "j" , "k" , "l" , "m" , "n" , "o" , "p" , "q" , "r" , "s" , "t" , "u" , "v" , "w" , "x" , "y" , "z" , "0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" , "_" ]
    white_space = ' '
    lexeme = ''
    lex =[]
    hash = False
    for i,char in enumerate(string):
        if char == '\n':
            hash = False
        if char == '#':
            hash = True
        if hash :
            continue
        if string[i] in symbols :
            lex.append(char)
        elif string[i] in skip :
            if lexeme != '' :
                lex.append(lexeme)
                lexeme = ''
        else :
            if char != white_space:
                lexeme += char # adding a char each time
            if (i+1 < len(string)): # prevents error
                if string[i+1] == white_space or string[i+1] in symbols or (lexeme in KEYWORDS and string[i+1] not in valid): # if next char == ' '
                    if lexeme != '':
                            if lexeme != '' :
                                lex.append(lexeme)
                                lexeme = ''
    if lexeme not in skip :
        if lexeme != '' :
            lex.append(lexeme)
            lexeme = ''
    print(lex)
    return lex

