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

    def __init__(self,result,leftPro,rightPro):
        self.result = result
        self.leftPro = leftPro
        self.rightPro = rightPro
    @property
    def tipe(self):
        return self.result

    @property
    def kiri(self):
        return self.leftPro

    @property
    def kanan(self):
        return self.rightPro

class Cell(object):
    listPR = []

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
    def tipes(self):
        types = []
        for p in self.listPR:
            types.append(p.result)
        return types

    @property
    def getRules(self):       
        return self.listPR


class Grammar(object):
    grammarRules = ListBahasa()
    parseTab = None
    panjang = 0
    token = []
    countTree = 0
    start = []
    
    def __init__(self, filename):
        self.grammarRules = ListBahasa()
        self.parseTab = None
        self.panjang = 0
        self.start = []
        file = open(filename)
        for line in file:
            if (line[0] == "#" or line[0] == "\n"):
                continue
            if (line[0] == "$" ):
                self.start.append(line.split("->")[1].rstrip().strip())
                continue
            a, b = line.split("->")
            self.grammarRules[b.rstrip().strip()]=a.rstrip().strip()
        
    def setRules(self,t):
        try:
            return self.grammarRules[t]
        except KeyError as r:
            return None
              
    def parse(self,sentence):
        self.countTree = 0
        self.token , Lanjut = lexer(sentence.replace("True", "1").replace("False", "1").replace("None", "1"))
        self.panjang = len(self.token)
        if Lanjut :
            self.parseTab = [ [Cell() for x in range(self.panjang - y)] for y in range(self.panjang) ]
            
            #Run yang pertama, cocokin sama terminal

            for x, t in enumerate(self.token):
                r = self.setRules(t)
                self.parseTab[0][x].appendProduksi("MAny",rules(t,None,None),None)
                if len(t.split())==1 :
                    self.parseTab[0][x].appendProduksi("Any",rules(t,None,None),None)
                if isVar(t) :
                    self.parseTab[0][x].appendProduksi("Var",rules(t,None,None),None)
                if isInt(t):
                    self.parseTab[0][x].appendProduksi("Int",rules(t,None,None),None)
                    self.parseTab[0][x].appendProduksi("Bool",rules(t,None,None),None)
                if isAtt(t):
                    self.parseTab[0][x].appendProduksi("Att",rules(t,None,None),None)
                if r != None:
                    for w in r: 
                        self.parseTab[0][x].appendProduksi(w,rules(t,None,None),None)
            
            
            #Run yang selanjutnya
            
            
            for l in range(2,self.panjang+1):
                for s in range(1,self.panjang-l+2):
                    self.parseTab[l-1][s-1].appendProduksi("MAny",None,None)
                    for p in range(1,l-1+1):
                        t1 = self.parseTab[p-1][s-1].getRules
                        t2 = self.parseTab[l-p-1][s+p-1].getRules
                                
                        for a in t1:
                            for b in t2:
                                r = self.setRules(str(a.tipe) + " " + str(b.tipe))
                                if r is not None:
                                    for w in r:
                                        self.parseTab[l-1][s-1].appendProduksi(w,a,b)
                                
            self.countTree = len(self.parseTab[self.panjang-1][0].tipes)
            if   (isanysame(self.parseTab[self.panjang-1][0].tipes,self.start)) :
                print("----------------------------------------")
                print("----------------Accepted----------------")
                print("----------------------------------------")
            else:
                print("----------------------------------------")
                print("--------------Syntax Error--------------")
                print("----------------------------------------")
        else:
            print("----------------------------------------")
            print("--------------Syntax Error--------------")
            print("----------------------------------------")
    
    def printParseTab(self):
        
        
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
        
        
        
        for row in reversed(self.parseTab):
            l = []
            for cell in row:
                l.append(cell.tipes)
            lines.append(l)
        
        lines.append(self.token)
        print('')
        print(tabulate(lines))
        print('')           
                
def isanysame(L1, L2):
    for i in L1:
        if i in L2:
            return True
    return False

def isAtt(r):
    return r[0] == '.'

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
    symbols = ['{', '}','(', ')', '[', ']', ">", "<", "!", '"', '*',"/", "+", "-","%", ':', ',',"'", '='] # Symbol yang dipisahkan
    KEYWORDS =keyword.kwlist
    KEYWORDS.append("range")
    skip = ["\n","","\t"]
    valid = [ "A" , "B" , "C" , "D" , "E" , "F" , "G" , "H" , "I" , "J" , "K" , "L" , "M" , "N" , "O" , "P" , "Q" , "R" , "S" , "T" , "U" , "V" , "W" , "X" , "Y" , "Z" , "a" , "b" , "c" , "d" , "e" , "f" , "g" , "h" , "i" , "j" , "k" , "l" , "m" , "n" , "o" , "p" , "q" , "r" , "s" , "t" , "u" , "v" , "w" , "x" , "y" , "z" , "0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" , "_" ] #Simbol khusus variabel
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
                lexeme += char 
            if (i+1 < len(string)): 
                if string[i+1] == white_space or string[i+1] in symbols or string[i+1] == '.' or (lexeme in KEYWORDS and string[i+1] not in valid): 
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

