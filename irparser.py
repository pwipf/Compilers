# Group 5
# Philip Wipf
# Evgenia Kolotiouk
# Lei Xiong
# CSCI 468
# 29 Apr 2016
# LittleScanner for Project Step 4

# This parser uses the irscanner.py module and a simple grammar to convert
# the Little IR code to Tiny code.

# Tiny instructions are stored up in this instructions list

instructions=[]
iraccepted = 1; # flag to be set to zero on error. Test at the end to determine output.

import ply.yacc as yacc
import ply.lex as lex

import irscanner
from irscanner import tokens



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
            | comparei
            | comparef
            | label_statement
            | jump'''
    pass

def p_syscall(p):
    '''syscall : SYSCALL operand newln'''

    if p[1]=='WRITEF':
        p[1]='WRITER'
    if p[1]=='READF':
        p[1]='READR'

    instructions.append('sys '+p[1].lower() +' '+p[2])
    pass

def p_move(p):
    '''move : MOVE operand operand newln'''

    instructions.append('move '+p[2]+' '+p[3])

def p_inst3(p):
    '''inst3 : INSTRUCTION3 operand operand operand newln'''

    instructions.append('move '+p[2]+' '+p[4])

    if(p[1]=='MULTI'):
        p[1]='MULI'
    if(p[1]=='MULTF'):
        p[1]='MULF'

    pre=p[1][0:3]
    if p[1][3]=='F':
        pre+='R'
    if p[1][3]=='I':
        pre+='I'

    instructions.append(pre.lower() +' '+p[3]+' '+p[4])
    pass

def p_comparei(p):
    '''comparei : COMPAREI operand operand label newln'''
    instructions.append('cmpi '+p[2]+' '+p[3])
    instructions.append('j'+p[1][0:2].lower()+' '+p[4])
    pass

def p_comparef(p):
    '''comparef : COMPAREF operand operand label newln'''
    instructions.append('cmpr '+p[2]+' '+p[3])
    instructions.append('j'+p[1][0:2].lower()+' '+p[4])
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

#def p_result(p):
#    '''result : IDENTIFIER
#        | temp#'''
#    p[0]=p[1]
#    pass

def p_variable(p):
    '''variable : IDENTIFIER'''
    p[0]=p[1]

def p_error(p):
    global iraccepted
    print("Syntax error in input!")
    print(p)
    iraccepted = 0;


irlexer =lex.lex(module=irscanner)
irparser = yacc.yacc(debug=False)

