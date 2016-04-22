# Group 5
# Philip Wipf
# Evgenia Kolotiouk
# Lei Xiong
# CSCI 468
# 2 Mar 2016
# Parser for Project Step 2 (updated for Step 3)

from __future__ import print_function # use python 3 style print statements
import sys
import ply.yacc as yacc



import scanner
import symboltable

tokens = scanner.tokens

accepted = 1; # flag to be set to zero on error. Test at the end to determine output.

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
    symboltable.decl_str(p[2],p[4])
    #print("call decl_str(",p[2],", ",p[4],")")
    
def p_str(p):
    '''str : STRINGLITERAL'''
    p[0]=p[1];
    pass
    
def p_var_decl(p):
    '''var_decl : var_type id_list ';' '''
    for s in p[2]:
        symboltable.decl_var(s,p[1])
        #print("call decl_var(",s,", ",p[1],")")
    pass
    
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
    symboltable.decl_var(p[2],p[1])

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
    symboltable.exit_function()
    
def p_start_of_func(p):
    '''start_of_func : FUNCTION any_type id'''
    symboltable.enter_function(p[3])

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

def p_assign_stmt(p):
    "assign_stmt : assign_expr ';'"
    pass

def p_assign_expr(p):
    '''assign_expr : id ASSIGN expr'''
    pass

def p_read_stmt(p):
    """read_stmt : READ '(' id_list ')' ';'"""
    pass

def p_write_stmt(p):
    """write_stmt : WRITE '(' id_list ')' ';'"""
    pass

def p_return_stmt(p):
    """return_stmt : RETURN expr ';'"""
    pass

def p_expr(p):
    '''expr : expr_prefix factor'''
    pass

def p_expr_prefix(p):
    '''expr_prefix : expr_prefix factor addop 
        | empty'''
    pass

def p_factor(p):
    '''factor : factor_prefix postfix_expr'''
    pass

def p_factor_prefix(p):
    '''factor_prefix : factor_prefix postfix_expr mulop 
        | empty'''
    pass

def p_postfix_expr(p):
    '''postfix_expr : primary 
        | call_expr'''
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
        | id 
        | INTLITERAL 
        | FLOATLITERAL'''
    pass

def p_addop(p):
    '''addop : '+' 
        | '-' '''
    pass

def p_mulop(p):
    '''mulop : '*' 
        | '/' '''
    pass

def p_if_stmt(p):
    '''if_stmt : start_if '(' cond ')' decl stmt_list else_part ENDIF'''
    symboltable.exit_block()
    
def p_start_if(p):
    '''start_if : IF'''
    symboltable.enter_block()

def p_else_part(p):
    '''else_part : start_else decl stmt_list 
        | empty'''
    if len(p) > 3:
        symboltable.exit_block()
    
def p_start_else(p):
    '''start_else : ELSE'''
    symboltable.enter_block()

def p_cond(p):
    '''cond : expr compop expr'''
    pass

def p_compop(p):
    '''compop : '<' 
        | '>' 
        | '=' 
        | NOT_EQUAL 
        | LESS_EQUAL 
        | GREATER_EQUAL'''
    pass

def p_while_stmt(p):
    '''while_stmt : start_while '(' cond ')' decl stmt_list end_while'''
    pass
    
def p_start_while(p):
    '''start_while : WHILE'''
    #print("enter")
    symboltable.enter_block()
    
def p_end_while(p):
    '''end_while : ENDWHILE'''
    #print("exit")
    symboltable.exit_block()

def p_error(p):
    global accepted
    #print("Syntax error in input!")
    accepted = 0;
    
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

    symboltable.enter_function("GLOBAL")
    
    parser.parse(data)

    symboltable.exit_function()
    
    if accepted:
        #print("Accepted")
        symboltable.print_table()
        
    else:
        #print("Not accepted")
        pass

