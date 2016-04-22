from __future__ import print_function # use python 3 style print statements
import sys
import ply.yacc as yacc



import irscanner

tokens = irscanner.tokens

accepted = 1; # flag to be set to zero on error. Test at the end to determine output.


def p_program(p):
    '''program : label_statement LINK newln inst_list RET newln'''
    instructions.append('sys halt')
    pass

def p_label_statement(p):
    '''label_statement : LABEL label newln'''
    instructions.append("label "+p[2])


def p_newln(p):
    '''newln : NEWLINE
            | empty'''
    pass

def p_inst_list(p):
    '''inst_list : inst_list inst
        | empty'''
    pass

def p_empty(p):
    '''empty :'''
    pass

def p_inst(p):
    '''inst : syscall
            | move
            | inst3
            | compare
            | jump'''
    pass

def p_syscall(p):
    '''syscall : SYSCALL result newln'''
    instructions.append('sys '+p[1].lower() +' '+p[2])
    pass

def p_move(p):
    '''move : MOVE operand result newln'''
    if p[1]=='STOREI':
        instructions.append('move '+p[2]+' '+p[3])
    else:
        instructions.append(p[1].lower() +' '+p[2]+' '+p[3])
    pass

def p_inst3(p):
    '''inst3 : INSTRUCTION3 operand operand result newln'''

    instructions.append('move '+p[2]+' '+p[4])
    s=p[1].lower()
    if p[1]=='MULTI':
        s='muli'
    if p[1]=='MULTF':
        s='mulf'
    instructions.append(s +' '+p[3]+' '+p[4])
    pass

def p_compare(p): # TODO need to figure out how to decide if it is a cmpi or cmpr (float or real)
                  # requires a symbol table I think
    '''compare : COMPARE operand operand label newln'''
    instructions.append('cmp '+p[2]+' '+p[3])
    instructions.append('j'+p[1].lower()+' '+p[4])
    pass

def p_jump(p):
    '''jump : JUMP label newln'''
    instructions.append('jmp '+p[2])
    pass

def p_label(p):
    '''label : IDENTIFIER'''
    p[0]=p[1]
    pass

def p_operand(p):
    '''operand : variable
                | temp
                | INTLITERAL
                | FLOATLITERAL
                | STRINGLITERAL'''
    p[0]=str(p[1])
    pass

def p_temp(p):
    '''temp : TEMPORARY'''
    p[0]='r'+p[1]

def p_result(p):
    '''result : IDENTIFIER
        | temp'''
    p[0]=p[1]
    pass

def p_variable(p):
    '''variable : IDENTIFIER'''
    p[0]=p[1]
    addvar(p[1])


def p_error(p):
    global accepted
    print("Syntax error in input!")
    accepted = 0;

def addvar(v):
    if not v in variables:
        variables.append(v)

variables=[]
instructions=[]


parser = yacc.yacc()

try:                        # attempt to open file, read it in, build lexer, feed it data,
    f=open(sys.argv[1],'r') # and iterate through resulting token list
except IndexError:
    print ("[pyacc] missing input file", file=sys.stderr)  # output to terminal even if STDOUT is redirected
except IOError:
    print ("[pyacc] cannot open", sys.argv[1], file=sys.stderr)
else:
    data=f.read()
    f.close()

#    symboltable.enter_function("GLOBAL")

    parser.parse(data)

#    symboltable.exit_function()

    if accepted:
        for a in variables:
            print('var',a)
        for a in instructions:
            print(a)

    else:
        print("Not accepted")
        pass

