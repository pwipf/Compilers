# Group 5
# Philip Wipf
# Evgenia Kolotiouk
# Lei Xiong
# CSCI 468
# 29 Apr 2016
# Parser for Project Step 4

# This is the main file that compiles LITTLE code into tiny code.
# This file contains the grammar rules for LITTLE and stores up instructions
#   in the irnodes list.
# When finished parsing the LITTLE code, the result is fed as a single string
#   to the IR parser which generates the TINY code.

from __future__ import print_function # use python 3 style print statements
import sys
import ply.yacc as yacc
import ply.lex as lex

import littlescanner
from littlescanner import tokens

from irparser import irparser,irlexer,instructions,iraccepted



irnodes = [] # list of IR instructions, appended to throughout the parser

littleaccepted = 1; # flag to be set to zero on error. Test at the end to determine output.


###################################################################### get next label, next temp
labelcount = 1;
def nextlabel():
    global labelcount
    label = "label"+str(labelcount)
    labelcount +=1
    return label

tempcount = 1;
def next_temp(type):
    global tempcount
    s='$T'+str(tempcount)
    add_var(s,type)
    tempcount+=1
    return s

###################################################################### a little stack for labels
labelstack=[]
def push_label(label):
    global labelstack
    labelstack.append(label)

def pop_label():
    global labelstack
    return labelstack.pop()

###################################################################### Symbol Table and Temporaries
variables = {}
vartemp={}
temporaries = {}
strings = {}
def add_var(name, type, str=None):
    global variables
    global vartemp
    global temporaries
    global strings
    if name[0] == '$':
        temporaries[name]=type
    else:
        if not name in variables:
            vartemp[name]=next_temp(type)
        variables[name]=type
        #temporaries[name]=type
    if type == 'STRING':
        strings[name]=str;

def get_type(name):
    global variables
    global temporaries
    if name[0] == '$':
        return temporaries[name]
    else:
        return variables[name]

def get_temporary(name):
    global vartemp
    return vartemp[name]

def get_string(name):
    global strings
    return strings[name]


#####################################################################################
####################################################################### START GRAMMAR
def p_program(p):
    '''program : PROGRAM id BEGIN pgm_body END'''
    pass

def p_id(p):
    '''id : IDENTIFIER'''
    p[0]=p[1]

def p_pgm_body(p):
    '''pgm_body : decl func_declarations'''
    pass

def p_decl(p):
    '''decl : string_decl decl
            | var_decl decl
            | empty'''
    pass

def p_empty(p):
    '''empty :'''
    pass

def p_string_decl (p):
    "string_decl : STRING id ASSIGN str ';'"
    add_var(p[2],'STRING',p[4])

def p_str(p):
    '''str : STRINGLITERAL'''
    p[0]=p[1];

def p_var_decl(p):
    '''var_decl : var_type id_list ';' '''
    for s in p[2]:
        add_var(s,p[1])

def p_var_type(p):
    '''var_type : FLOAT
                | INT'''
    p[0]=p[1]

def p_any_type(p):
    '''any_type : var_type
                | VOID'''
    pass

def p_id_list(p):
    '''id_list : id id_tail'''
    p[0]=[p[1]] + p[2]

def p_id_tail(p):
    """id_tail : ',' id id_tail
                | empty"""
    if len(p) > 2: # not empty
        p[0]=[p[2]] + p[3]
    else:
        p[0]=[]

def p_param_decl_list(p):
    '''param_decl_list : param_decl param_decl_tail
                | empty'''
    pass

def p_param_decl(p):
    '''param_decl : var_type id '''
    add_var(p[2],p[1])

def p_param_decl_tail(p):
    """param_decl_tail : ',' param_decl param_decl_tail
        | empty"""
    pass

def p_func_declarations(p):
    '''func_declarations : func_decl func_declarations
        | empty'''
    pass

def p_func_decl(p):
    """func_decl : start_of_func '(' param_decl_list ')' BEGIN func_body END"""
    irnodes.append('RET')

def p_start_of_func(p):
    '''start_of_func : FUNCTION any_type id'''

    irnodes.append('LABEL '+ p[3])
    irnodes.append('LINK')

def p_func_body(p):
    '''func_body : decl stmt_list'''
    pass

def p_stmt_list(p):
    '''stmt_list : stmt stmt_list
        | empty'''
    pass

def p_stmt(p):
    '''stmt : base_stmt
        | if_stmt
        | while_stmt'''
    pass

def p_base_stmt(p):
    '''base_stmt : assign_stmt
        | read_stmt
        | write_stmt
        | return_stmt'''
    pass

####################################################################### assignments
def p_assign_stmt(p):
    "assign_stmt : assign_expr ';'"
    pass

def p_assign_expr(p):
    '''assign_expr : id ASSIGN expr'''

    type = get_type(p[1])
    ending = type[0]

    irnodes.append('STORE'+ending+' '+ p[3]+' '+get_temporary(p[1])) # directly assign value to temporary of id

####################################################################### read/write
def p_read_stmt(p):
    """read_stmt : READ '(' id_list ')' ';'"""
    for i in p[3]:
        type=get_type(i)
        ending=type[0]
        irnodes.append('READ'+ending+' '+get_temporary(i))

def p_write_stmt(p):
    """write_stmt : WRITE '(' id_list ')' ';'"""
    for i in p[3]:
        type=get_type(i)
        ending=type[0]
        if not ending=='S':
            irnodes.append('STORE'+ending+' '+get_temporary(i)+' '+i)

        irnodes.append('WRITE'+ending+' '+i)

def p_return_stmt(p):
    """return_stmt : RETURN expr ';'"""
    pass

####################################################################### Expressions
def p_expr(p):
    '''expr : expr_prefix factor'''

    if p[1]==[]:    # no expr_prefix, return factor (could be temp register or id)
        p[0] = p[2]

    else:           # has expr_prefix, get type and output the add or subtract statements
        if get_type(p[2])=='INT':
            type='INT'
            ending='I'
        elif get_type(p[2])=='FLOAT':
            type='FLOAT'
            ending='F'

        if len(p[1])==1:    # expr_prefix is a list of length 1, just output the single add
            t=next_temp(type)
            irnodes.append(p[1][0][1]+ending+' '+ p[1][0][0]+' '+ p[2]+' '+ t)

        else:               # more than one item to add up in expr_prefix, have to loop through them
            t=next_temp(type)

            fp=p[1][0]
            fpnext=p[1][1]
            op=fp[1]+ending
            irnodes.append(op+' '+ fp[0]+' '+ fpnext[0]+' '+ t)
            op=fpnext[1]+ending

            for fp in p[1][2:]:
                lastop=op
                op=fp[1]+ending
                lastt=t
                t=next_temp(type)
                irnodes.append(lastop+' '+ lastt+' '+ fp[0]+' '+ t)

            lastt=t
            t=next_temp(type)
            irnodes.append(op+' '+ lastt+' '+ p[2]+' '+ t)

        # return result (temp register)
        p[0]=t



def p_expr_prefix(p):
    '''expr_prefix : expr_prefix factor addop
        | empty'''

    if len(p) == 2:
        p[0]=[]
    else:
        p[0]=p[1]+[[p[2],p[3]]]

def p_factor(p):
    '''factor : factor_prefix postfix_expr'''

    if p[1]==[]:
        p[0]=p[2]

    else:
        if get_type(p[2])=='INT':
            type='INT'
            ending='I'
        elif get_type(p[2])=='FLOAT':
            type='FLOAT'
            ending='F'

        if len(p[1])==1:
            t=next_temp(type)
            irnodes.append(p[1][0][1]+ending+' '+ p[1][0][0]+' '+ p[2]+' '+ t)

        else:


            t=next_temp(type)

            fp=p[1][0]
            fpnext=p[1][1]
            op=fp[1]+ending
            irnodes.append(op, fp[0], fpnext[0], t)
            op=fpnext[1]+ending

            for fp in p[1][2:]:
                lastop=op
                op=fp[1]+ending
                lastt=t
                t=next_temp(type)
                irnodes.append(lastop+' '+ lastt+' '+ fp[0]+' '+ t)

            lastt=t
            t=next_temp(type)
            irnodes.append(op+' '+ lastt+' '+ p[2]+' '+ t)

        p[0]=t


def p_factor_prefix(p):
    '''factor_prefix : factor_prefix postfix_expr mulop
        | empty'''

    if len(p) == 2:
        p[0]=[]
    else:
        p[0]=p[1]+[[p[2],p[3]]]

def p_postfix_expr(p):
    '''postfix_expr : primary
        | call_expr'''

    p[0]=p[1]
    pass

def p_call_expr(p):
    """call_expr : id '(' expr_list ')'"""
    pass

def p_expr_list(p):
    '''expr_list : expr expr_list_tail
        | empty'''
    pass

def p_expr_list_tail(p):
    '''expr_list_tail : ',' expr expr_list_tail
        | empty'''
    pass

def p_primary(p):
    '''primary : '(' expr ')'
                | idlit
                | intlit
                | floatlit'''

    if p[1] == '(':
        p[0]=p[2]
    else:
        p[0]=p[1]


def p_intlit(p):
    '''intlit : INTLITERAL'''
    t=next_temp('INT')
    irnodes.append("STOREI"+' '+str(p[1])+' '+t)
    p[0]=t

def p_floatlit(p):
    '''floatlit : FLOATLITERAL'''
    t=next_temp('FLOAT')
    irnodes.append("STOREF"+' '+str(p[1])+' '+t)
    p[0]=t

def p_idlit(p):
    '''idlit : id'''

    p[0]=get_temporary(p[1])

def p_addop(p):
    '''addop : '+'
        | '-' '''
    if p[1]=='+':
        p[0]='ADD'
    else:
        p[0]='SUB'

def p_mulop(p):
    '''mulop : '*'
        | '/' '''
    if p[1]=='*':
        p[0]='MULT'
    else:
        p[0]='DIV'

####################################################################### IF THEN ELSE
def p_if_stmt(p):
    '''if_stmt : start_if decl stmt_list else_part ENDIF'''

    irnodes.append('LABEL '+pop_label())

def p_start_if(p):
    '''start_if : IF '(' cond ')' '''

    label = nextlabel() #else label
    push_label(label)

    #code for condition, label is else_part
    irnodes.append(p[3][0]+' '+p[3][1]+' '+p[3][2]+' '+label)

    label = nextlabel() #end end label
    push_label(label)

def p_else_part(p):
    '''else_part : start_else decl stmt_list
        | empty'''

    if len(p) < 3:
        pop_label()

def p_start_else(p):
    '''start_else : ELSE'''

    lab=pop_label()
    irnodes.append('JUMP '+lab)
    irnodes.append('LABEL '+pop_label())
    push_label(lab)


####################################################################### CONDITIONS
def p_cond(p):
    '''cond : expr compop expr'''

    type = get_type(p[1])
    ending = type[0]

    if not p[3][0]=='$':   #second expr can't be an id
        t=next_temp(type)
        irnodes.append('STORE'+ending+' '+p[3]+' '+t)
        p[3]=t

    p[0]=[p[2]+ending, p[1], p[3]]

def p_compop(p):
    '''compop : '<'
        | '>'
        | '='
        | NOT_EQUAL
        | LESS_EQUAL
        | GREATER_EQUAL'''
    not_ops = {
        "<" : "GE",
        ">" : "LE",
        "!=" : "EQ",
        "=" : "NE",
        "<=" : "GT",
        ">=" : "LT"
    }
    p[0] = not_ops[p[1]]
    pass

####################################################################### WHILE
def p_while_stmt(p):
    '''while_stmt : start_while decl stmt_list end_while'''
    irnodes.append("JUMP"+' '+pop_label())
    irnodes.append("LABEL"+' '+pop_label())
    pass

def p_start_while(p):
    '''start_while : WHILE '(' cond ')' '''
    #symboltable.enter_block()

    label1 = nextlabel()
    irnodes.append("LABEL"+' '+ label1)
    label2 = nextlabel()
    #condition code:
    irnodes.append(p[3][0]+' '+p[3][1]+' '+p[3][2]+' '+label2)
    push_label(label2)
    push_label(label1)

def p_end_while(p):
    '''end_while : ENDWHILE'''
    #symboltable.exit_block()



####################################################################### ERROR
def p_error(p):
    global littleaccepted
    #print("Syntax error in input!")
    littleaccepted = 0;
####################################################################### END GRAMMAR
###################################################################################

littlelexer = lex.lex(module=littlescanner)
littleparser = yacc.yacc(debug=False)


# attempt to open file, read it in, parse it
try:
    f=open(sys.argv[1],'r')
except IndexError:
    print ("[pyacc] missing input file", file=sys.stderr)  # output to terminal even if STDOUT is redirected
except IOError:
    print ("[pyacc] cannot open", sys.argv[1], file=sys.stderr)
else:
    data=f.read()
    f.close()

    littleparser.parse(data)

    # string to store all the IR instructions, fed to IR parser to generate the tiny code
    irdata=''

    if littleaccepted:

        # just to show the variables/temporaries list
        for i in variables:
            if variables[i]=='STRING':
                print(';',i,variables[i],vartemp[i],temporaries[vartemp[i]],strings[i])
            else:
               print(';',i,variables[i],vartemp[i],temporaries[vartemp[i]])

        # fill irdata string with data for IR parser
        for i in irnodes:
            irdata+= i+'\n'
            print(';',i)

        # parse the IR code
        irparser.parse(irdata, lexer=irlexer)

        if iraccepted:

            # output the variables and strings for tiny code variable declarations
            for s in variables:
                if variables[s] == 'STRING':
                    print('str',s,strings[s])
                else:
                    print('var',s)

            # output the actual tiny instructions
            for i in instructions:
                print(i)


        else:
            print("IR code Not accepted")

    else:
        print("Little code Not accepted")

