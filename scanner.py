# Group 5
# Philip Wipf
# Evgenia Kolotiouk
# Lei Xiong
# CSCI 468
# 10 Feb 2016
# Scanner for Project Step 1
#   Modified to work with Step 2 parser 
#   (added literals and added keywords and duals to tokens)
#   (Also made the type equal to the value for keywords, instead of type='KEYWORD')


from __future__ import print_function # use python 3 style print statements
import sys
from ply import *

literals = ['+','-','*','/','(',')',';',',','=','<','>']

duals = (
    'ASSIGN',
    'NOT_EQUAL',
    'LESS_EQUAL',
    'GREATER_EQUAL',
    )

keywords = (        # this list allows identifiers to be flagged as keywords if in this list
    'PROGRAM',
    'BEGIN',
    'END',
    'FUNCTION',
    'READ',
    'WRITE',
    'IF',
    'ELSE',
    'ENDIF',
    'WHILE',
    'ENDWHILE',
    'RETURN',
    'INT',
    'VOID',
    'STRING',
    'FLOAT',
    )
    
tokens = keywords + duals + (          # tokens list, every token returned MUST end up with a type in this list
    'IDENTIFIER',
    'INTLITERAL',
    'FLOATLITERAL',
    'STRINGLITERAL',
    )
    
t_ignore = ' \t'            # ignore and skip over spaces and tabs (special variable name)
    
t_ASSIGN = r':='
t_NOT_EQUAL = r'!='
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='

def t_COMMENT(t):           # COMMENT must be before OPERATOR or the dashes will be seen as -
    r'--.*'                 # note: . matches any char EXCEPT \n
    pass

#def t_OPERATOR(t):          # alternations in proper order to match < only if not <=
#    r':=|\+|-|\*|/|!=|\(|\)|;|,|<=|>=|=|<|>'
#    return t

def t_FLOATLITERAL(t):      # FLOAT must be before INT or 1.4 will be seen as 1, 0.4
    r'(\d+\.\d*|\d*\.\d+)'  # allow xx. OR .xx NOT .
    t.value=float(t.value)
    return t
    
def t_INTLITERAL(t):
    r'\d+'
    t.value=int(t.value)
    return t
    
def t_STRINGLITERAL(t):
    r'".*?"'                # need greedy (?) modifier on * to disallow "str"ing"
    return t
    
def t_IDENTIFIER(t):        # keywords match here also so check if the identifier is in
    r'[a-zA-Z][a-zA-Z0-9]*' # the keyword list
    if t.value in keywords:
        t.type=t.value
    return t
    
def t_newline(t):           # need to match newlines, in theory they could probably be ignored,
    r'\n|\r\n'              # but this function allows keeping track of line numbers.
    t.lexer.lineno+=1       # note nothing returned. (arbitrary function name)
    
def t_error(t):             # anything not matched so far is an error (special function name)
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()

try:                        # attempt to open file, read it in, build lexer, feed it data,
    f=open(sys.argv[1],'r') # and iterate through resulting token list
except IndexError:
    print ("missing input file", file=sys.stderr)  # output to terminal even if STDOUT is redirected
except IOError:
    print ("cannot open", sys.argv[1], file=sys.stderr)
else:
    data=f.read()
    f.close()

    lexer = lex.lex() 
    lexer.input(data)

#    for token in lexer:
#        print ("Token Type:", token.type)
#        print ("Value:", token.value)
