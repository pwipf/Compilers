# Group 5
# Philip Wipf
# Evgenia Kolotiouk
# Lei Xiong
# CSCI 468
# 31 Mar 2016
# Symbol Table for Project Step 3

symbol_table = {}

scope_stack = []
history_list = []

counter = 1
current_scope = ""
def enter_function(name):
    scope_stack.append(name)
    global current_scope
    current_scope = name
    symbol_table[name] = {}
    if not current_scope == "GLOBAL":
        history_list.append("")
    history_list.append("Symbol table " + current_scope)

def exit_function():
    name = scope_stack.pop()
    symbol_table.pop(name)

def enter_block():
    global counter
    name = "BLOCK " + str(counter)
    scope_stack.append(name)
    counter += 1
    global current_scope
    current_scope = name
    symbol_table[name] = {}
    history_list.append("")
    history_list.append("Symbol table " + current_scope)

def exit_block():
    name = scope_stack.pop()
    symbol_table.pop(name)

def decl_str(name,value):
    add_to_table(name,"STRING",current_scope,value)
    history_list.append("name " + name + " type STRING value " + value)

def decl_var(name,type):
    add_to_table(name, type, current_scope, 0)
    history_list.append("name "+ name + " type " + type)

is_error_existed = 0

def add_to_table(var_name,var_type,scope_name,var_value):
    global is_error_existed
    if symbol_table[scope_name].__contains__(var_name):
        if not is_error_existed:
            print("DECLARATION ERROR " + str(var_name))
            is_error_existed = 1
    else:
        symbol_table[scope_name][var_name] = {
            var_name: {
                "var_name": var_name,
                "var_type": var_type,
                "value": var_value
            }
        }

def print_table():
    if is_error_existed:
        pass
    else:
        for item in history_list:
            print(item)
