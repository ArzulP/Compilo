import ply.yacc as yacc

from lex import tokens
import AST

def p_programme_statement(p):
    ''' programme : expression '''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : expression NEWLINE programme '''
    p[0] = AST.ProgramNode([p[1]]+p[3].children)

def p_expression_mov(p):
    '''expression :  MOV expression ',' expression'''
    p[0] = AST.OpNode(p[1], [p[2], p[4]])

def p_expression_push(p):
    '''expression :  PUSH expression'''
    p[0] = AST.PushNode(p[2])

def p_expression_pop(p):
    '''expression :  POP expression'''
    p[0] = AST.PopNode(p[2])
    	
def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")


precedence = (
    ('left', 'MOV'),
    ('left', 'PUSH'),
    ('left', 'POP'),
)

yacc.yacc(outputdir='generated')

def parse(program):
    return yacc.parse(program)


if __name__ == "__main__":
    import sys 
    	
    prog = open(sys.argv[1]).read()
    result = parse(prog)
    if result:
        print (result)
    else:
        print ("Parsing returned no result!")