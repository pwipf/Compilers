# Compilers course

This Python project uses David Beazley's [PLY (Python Lex Yacc)](http://www.dabeaz.com/ply/)  library to scan and parse a simple imperative programming language called LITTLE.  The grammar for the language is described in the file [little_grammar.txt](/little_grammar.txt).  

The main module is littleparser.py, which uses the other modules and the PLY modules to compile the LITTLE source code to an intermediate representation, and then convert that IR code to assembly instructions which will run on the TINY simulator, included as tinyNew.C (this can easily be compiled with G++).

The "StepX" folders have test files for checking the output as we progressed through
- (1) scanning the language for tokens, 
- (2) parsing the tokens checking for a valid program, 
- (3) creating a symbol table with scope stack, and 
- (4) generating the code.  

Usage:  
- The input to littleparser.py is the source to a LITTLE program, the output is a text file containing lines of "tiny" assembly instructions (also has the IR instructions, commented out for the tiny simulator with ';').
- The input to the tiny simulator is the output of littleparser.py.

For example, if tinyNew.C is compiled to tiny.exe, and your LITTLE source file is program1.txt, you could run:  
- python littleparser.py program1.txt > program1.tiny
- ./tiny program1.tiny

This would save the output of littleparser.py to a text file, program1.tiny, and then run the tiny simulator on that text file.
