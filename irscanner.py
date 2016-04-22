# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from __future__ import print_function # use python 3 style print statements
import sys
from ply import *



instruction3 = (
    'ADDI',
    'ADDF',
    'SUBI',
    'SUBF',
    'MULTI',
    'MULTF',
    'DIVI',
    'DIVF',
    )

compare = (
    'GT',
    'GE',
    'LT',
    'LE',
    'NE',
    'EQ'
    )

move=(
    'STOREI',
    'STOREF',
    'STORES'
    )
syscall=(
    'WRITEI',
    'WRITEF',
    'WRITES',
    'READI',
    'READF',
    'READS'
    )
keywords=(
    'JUMP',
    'LABEL',
    'LINK',
    'RET'
    )

tokens = syscall + move + instruction3 + compare + keywords + (          # tokens list, every token returned MUST end up with a type in this list
    'IDENTIFIER',
    'INTLITERAL',
    'FLOATLITERAL',
    'STRINGLITERAL',
    'TEMPORARY',
    'NEWLINE',
    'SYSCALL',
    'MOVE',
    'INSTRUCTION3',
    'COMPARE'
    )

t_ignore = ' \t'            # ignore and skip over spaces and tabs (special variable name)


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
    if t.value in syscall:
        t.type='SYSCALL'
    if t.value in move:
        t.type='MOVE'
    if t.value in instruction3:
        t.type='INSTRUCTION3'
    if t.value in keywords:
        t.type=t.value
    if t.value in compare:
        t.type='COMPARE'
    return t

def t_TEMPORARY(t):
    r'\$T\d+'
    s=t.value.replace('$T','')
    i=int(s)-1
    t.value=str(i)
    return t

def t_NEWLINE(t):           # need to match newlines, in theory they could probably be ignored,
    r'\n|\r\n'              # but this function allows keeping track of line numbers.
    t.lexer.lineno+=1       # note nothing returned. (arbitrary function name)
    t.value='\\n'
    return t

def t_error(t):             # anything not matched so far is an error (special function name)
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()
#
#try:                        # attempt to open file, read it in, build lexer, feed it data,
#    f=open('test.txt','r') # and iterate through resulting token list
#except IndexError:
#    print ("missing input file", file=sys.stderr)  # output to terminal even if STDOUT is redirected
#except IOError:
#    print ("cannot open", sys.argv[1], file=sys.stderr)
#else:
#    data=f.read()
#    f.close()
#
#    lexer = lex.lex()
#    lexer.input(data)
#
#    for token in lexer:
#        print ("Token Type:", token.type)
#        print ("Value:", token.value)
