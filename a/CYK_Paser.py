import keyword

class ListBahasa(dict):
    
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(ListBahasa, self).__setitem__(key, [])
        self[key].append(value)


class rules(object):
    
    result = None
    leftPro = None
    rightPro = None
    
    #Parameters:
    #   Result: String
    #   leftPro: Production rule (left child of the production rule)
    #   rightPro: Production rule (right child of the production rule)
    def __init__(self,result,leftPro,rightPro):
        self.result = result
        self.leftPro = leftPro
        self.rightPro = rightPro
    
    #Returns the result of the production rule, VP, S, NP... 
    def tipe(self):
        return self.result
    
    #Returns the left child of the production rule
    def kiri(self):
        return self.leftPro
    
    #Returns the right child of the production rule
    def kanan(self):
        return self.rightPro

class Cell(object):
    listPR = []
    
    
    #Parameters:
    #   Productions: List of production rules
    
    def __init__(self, listPR=None):
        if listPR is None:
            self.listPR = []
        else:
            self.listPR = listPR
            
    def appendProduksi(self, result,leftPro,rightPro):
        self.listPR.append(rules(result,leftPro,rightPro))
    
    def konfProduksi(self, p):
        self.listPR = p
    
    @property
    def tipe(self):
        types = []
        for p in self.listPR:
            types.append(p.result)
        return types
    @property
    def get_rules(self):       
        return self.listPR


class Grammar(object):
    
    grammar_rules = ListBahasa()
    parse_table = None
    length = 0
    tokens = []
    number_of_trees = 0
    start = []
    
    #Parameters:
    #   Filename: file containing a grammar
    
    def __init__(self, filename):
        self.grammar_rules = ListBahasa()
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
        self.tokens, Lanjut = lexer(sentence.replace("True", "1").replace("False", "1").replace("None", "1"))
        if Lanjut :
            self.length = len(self.tokens)
            if self.length < 1:
                raise ValueError("The sentence could no be read")
            self.parse_table = [ [Cell() for x in range(self.length - y)] for y in range(self.length) ]
            
            
            #Process the first line
            for x, t in enumerate(self.tokens):
                r = self.apply_rules(t)
                self.parse_table[0][x].appendProduksi("MAny",rules(t,None,None),None)
                if len(t.split())==1 :
                    self.parse_table[0][x].appendProduksi("Any",rules(t,None,None),None)
                if isVar(t) :
                    self.parse_table[0][x].appendProduksi("Var",rules(t,None,None),None)
                if isInt(t):
                    self.parse_table[0][x].appendProduksi("Int",rules(t,None,None),None)
                    self.parse_table[0][x].appendProduksi("Bool",rules(t,None,None),None)
                if r != None:
                    for w in r: 
                        self.parse_table[0][x].appendProduksi(w,rules(t,None,None),None)
            
            
            #Run CYK-Parser
            
            
            for l in range(2,self.length+1):
                for s in range(1,self.length-l+2):
                    self.parse_table[l-1][s-1].appendProduksi("MAny",None,None)
                    for p in range(1,l-1+1):
                        t1 = self.parse_table[p-1][s-1].get_rules
                        t2 = self.parse_table[l-p-1][s+p-1].get_rules
                        for a in t1:
                            for b in t2:
                                #print(a,b,r)
                                r = self.apply_rules(str(a.tipe) + " " + str(b.tipe))
                                if r is not None:
                                    for w in r:
                                        #print('Applied Rule: ' + str(w) + '[' + str(l) + ',' + str(s) + ']' + ' --> ' + str(a.tipe) + '[' + str(p) + ',' + str(s) + ']' + ' ' + str(b.tipe)+ '[' + str(l-p) + ',' + str(s+p) + ']')
                                        self.parse_table[l-1][s-1].appendProduksi(w,a,b)
                                
            self.number_of_trees = len(self.parse_table[self.length-1][0].tipe)
            if   (isanysame(self.parse_table[self.length-1][0].tipe,self.start)) :
                print("----------------------------------------")
                print('The sentence IS accepted in the language')
                print('Number of possible trees: ' + str(self.number_of_trees))
                print("----------------------------------------")
                
            else:
                print("--------------------------------------------")
                print('The sentence IS NOT accepted in the language')
                print("--------------------------------------------")
        else :
            print("--------------------------------------------")
            print('The sentence IS NOT accepted in the language')
            print("--------------------------------------------")
        
        
    #Returns a list containing the parent of the possible trees that we can generate for the last sentence that have been parsed
    def get_trees(self):
        return self.parse_table[self.length-1][0].listPR
                
                
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
                l.append(cell.tipe)
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
    loop = False
    cdil = False
    deff = False
    brconpas = False
    cond = False
    cond0 = 0
    for i,char in enumerate(string):
        if char == '\n':
            hash = False
            brconpas = False
        if char == '#':
            hash = True
            brconpas = False
        if hash :
            continue
        if brconpas :
            if char not in skip and char != white_space :
                return [], False
        if string[i] in symbols :
            lex.append(char)
        elif string[i] in skip :
            if lexeme != '' :
                if lexeme == "for" or lexeme == "while" :
                    loop = True
                    cdil = True
                if lexeme == "if" :
                    cond = True
                    cond0 += 1
                    cdil = True
                if lexeme == "def":
                    deff = True
                    cdil = True
                if lexeme == "class":
                    cdil = True
                if lexeme == "break" or lexeme == "continue" :
                    brconpas = True
                    if not (loop) :
                        return [] , False
                if lexeme == "return":
                    hash = True
                    if not deff :
                        return [] , False
                if lexeme == "pass" and not cdil :
                    brconpas = True
                    return [], False
                if lexeme == "elif" and not cond:
                    return [], False
                if lexeme == "else" :
                    if cond0<=0:
                        return [], False
                    else:
                        cond0 -= 1
                lex.append(lexeme)
                lexeme = ''
        else :
            if char != white_space:
                lexeme += char # adding a char each time
            if (i+1 < len(string)): # prevents error
                if string[i+1] == white_space or string[i+1] in symbols or (lexeme in KEYWORDS and string[i+1] not in valid): # if next char == ' '
                    if lexeme != '':
                            if lexeme != '' :
                                if lexeme == "for" or lexeme == "while" :
                                    loop = True
                                    cdil = True
                                if lexeme == "if" :
                                    cond = True
                                    cond0 += 1
                                    cdil = True
                                if lexeme == "def":
                                    deff = True
                                    cdil = True
                                if lexeme == "class":
                                    cdil = True
                                if lexeme == "break" or lexeme == "continue" :
                                    brconpas = True
                                    if not (loop) :
                                        return [] , False
                                if lexeme == "return":
                                    hash = True
                                    if not deff :
                                        return [] , False
                                if lexeme == "pass" and not cdil :
                                    brconpas = True
                                    return [], False
                                if lexeme == "elif" and not cond:
                                    return [], False
                                if lexeme == "else":
                                    if cond0<=0:
                                        return [], False
                                    else:
                                        cond0 -= 1
                                lex.append(lexeme)
                                lexeme = ''
    if lexeme not in skip :
        if lexeme != '' :
            lex.append(lexeme)
            lexeme = ''
    print(lex)
    return lex , True

