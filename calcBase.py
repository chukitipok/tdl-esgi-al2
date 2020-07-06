# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------

from Arbre.evals import evalInst
from Arbre.genereTreeGraphviz2 import printTreeGraph

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'print': 'PRINT',
    'func': "FUNCTION"
}

tokens = [
             'NUMBER', 'MINUS',
             'PLUS', 'TIMES', 'DIVIDE', 'MOD',
             'LPAREN', 'RPAREN',
             'AND', 'OR', 'INF', 'INFEQUAL', 'SUP', 'SUPEQUAL', 'DIFF', 'EQUAL',
             'SEMICOLON', 'COMA', 'NAME', 'AFFECT', 'LACCO', 'RACCO',
         ] + list(reserved.values())

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LACCO = r'\{'
t_RACCO = r'\}'
t_AND = r'&'
t_OR = r'\|'
t_SEMICOLON = r';'
t_COMA = r','
t_AFFECT = r'='
t_INF = r'<'
t_INFEQUAL = r'<='
t_SUP = r'>'
t_SUPEQUAL = r'>='
t_EQUAL = r'=='
t_DIFF = r'!='

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'INF', 'SUP', 'INFEQUAL', 'SUPEQUAL', 'EQUAL', 'DIFF'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
)


def t_NAME(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    t.type = reserved.get(t.value, 'NAME')  # Check for reserved words
    return t


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lex.lex()


def p_start(t):
    """ start : block
        | body"""
    t[0] = ('Program', t[1])
    evalInst(t[0])
    print(t[0])
    # printTreeGraph(t[0])


# def p_instruction(p):
#     """instruction : statement"""
#     p[0] = p[1]


def p_if(p):
    """statement : IF LPAREN expression RPAREN block"""
    p[0] = ('If', p[3], p[5])


def p_if_else(p):
    """statement : IF LPAREN expression RPAREN block ELSE block"""
    p[0] = ('If Else', p[3], p[5], p[7])


def p_while(p):
    """statement : WHILE LPAREN expression RPAREN block"""
    p[0] = ('While', p[3], p[5])


def p_for(p):
    """statement : FOR LPAREN statement expression SEMICOLON statement RPAREN block"""
    p[0] = ('For', p[3], p[4], p[6], p[8])


def p_call_function(p):
    """statement : NAME LPAREN params RPAREN SEMICOLON"""
    p[0] = ('Call', p[1], p[3])


def p_call_function_no_args(p):
    """statement : NAME LPAREN RPAREN SEMICOLON"""
    p[0] = ('Call', p[1], ('Arg',))


def p_argument(p):
    """args : NAME"""
    p[0] = ('Arg', p[1])


def p_arguments(p):
    """args : NAME COMA args"""
    p[0] = ('Arg', p[1], *p[3][1::])


def p_param(p):
    """params : expression"""
    p[0] = ('Param', p[1])


def p_params(p):
    """params : expression COMA params"""
    p[0] = ('Param', p[1], *p[3][1::])


def p_function_with_args(p):
    """statement : FUNCTION NAME LPAREN args RPAREN block"""
    p[0] = ('Function', p[2], p[4], p[6])


def p_function_no_args(p):
    """statement : FUNCTION NAME LPAREN RPAREN block"""
    p[0] = ('Function', p[2], ('Arg',), p[5])


def p_instruction(p):
    """body : statement"""
    p[0] = ('Block', p[1])


def p_instructions(p):
    """body : statement body"""
    p[0] = ('Block', p[1], p[2])
    print(p[0])


def p_block(p):
    """block : LACCO body RACCO"""
    p[0] = ('Block', p[2])


def p_block_empty(p):
    """block : LACCO RACCO"""
    p[0] = ('Block', )


def p_print(p):
    """statement : PRINT LPAREN expression RPAREN SEMICOLON"""
    p[0] = ('Print', p[3])


def p_expression_binop_plus(p):
    """expression : expression PLUS expression"""
    p[0] = ('+', p[1], p[3])


def p_expression_binop_times(p):
    """expression : expression TIMES expression"""
    p[0] = ('*', p[1], p[3])


def p_expression_binop_minus(p):
    """expression : expression MINUS expression"""
    p[0] = ('-', p[1], p[3])


def p_expression_binop_divide(p):
    """expression : expression DIVIDE expression"""
    p[0] = ('/', p[1], p[3])


def p_expression_binop_mod(p):
    """expression : expression MOD expression"""
    p[0] = ('%', p[1], p[3])


def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_expression_name(p):
    """expression : NAME"""
    p[0] = p[1]


def p_expression_binop_bool(p):
    """expression : expression AND expression
                | expression OR expression
                | expression INF expression
                | expression INFEQUAL expression
                | expression SUP expression
                | expression SUPEQUAL expression
                | expression DIFF expression
                | expression EQUAL expression"""
    p[0] = (p[2], p[1], p[3])


def p_statement_increment(p):
    """statement : NAME PLUS PLUS
        | NAME PLUS PLUS SEMICOLON"""
    p[0] = ('Affect', p[1], ('+', p[1], 1))


def p_statement_decrement(p):
    """statement : NAME MINUS MINUS
        | NAME MINUS MINUS SEMICOLON"""
    p[0] = ('Affect', p[1], ('-', p[1], 1))


def p_expression_affectation(p):
    """statement : NAME AFFECT expression
        | NAME AFFECT expression SEMICOLON"""
    p[0] = ('Affect', p[1], p[3])


def p_error(p):
    print(f"Syntax error at {p}")


import ply.yacc as yacc

yacc.yacc()

s = input('calc > ')

# file = open("fibonacci.txt")
# s = file.read()

yacc.parse(s)
