# Group 5
# Philip Wipf
# Evgenia Kolotiouk
# Lei Xiong
# CSCI 468
# 29 Apr 2016
# LittleScanner for Project Step 4

# This file is just holds scanner definitions for the Little language IR scanner
# (for converting Little IR to Tiny

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

comparei = (
    'GTI',
    'GEI',
    'LTI',
    'LEI',
    'NEI',
    'EQI'
    )

comparef = (
    'GTF',
    'GEF',
    'LTF',
    'LEF',
    'NEF',
    'EQF'
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

tokens = keywords + (# tokens list, every token returned MUST end up with a type in this list
    'IDENTIFIER',
    'INTLITERAL',
    'FLOATLITERAL',
    'STRINGLITERAL',
    'TEMPORARY',
    'NEWLINE',
    'SYSCALL',
    'MOVE',
    'INSTRUCTION3',
    'COMPAREI',
    'COMPAREF'
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
    if t.value in comparei:
        t.type='COMPAREI'
    if t.value in comparef:
        t.type='COMPAREF'
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

