import keyword

symbols = ['{', '}', '(', ')', '[', ']', '.', '"', '*', '\n', ':', ','] # single-char keywords
other_symbols = ['\\', '/*', '*/'] # multi-char keywords
keywords = ['public', 'class', 'void', 'main', 'String', 'int']
KEYWORDS =keyword.kwlist

string = "Aku ins(ang kamu"

white_space = ' '
lexeme = ''
lex =[]
for i,char in enumerate(string):
    if string[i] in symbols :
        lex.append(char)
    else :
        if char != white_space:
            lexeme += char # adding a char each time
        if (i+1 < len(string)): # prevents error
            if string[i+1] == white_space or string[i+1] in symbols or lexeme in KEYWORDS: # if next char == ' '
                if lexeme != '':
                    lex.append(lexeme)
                    lexeme = ''


print (lex)