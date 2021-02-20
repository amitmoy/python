from sly import Lexer
from Utilities import Constants, is_int, Expression


class CpqLexer(Lexer):

    tokens = {BREAK, CASE, DEFAULT, ELSE, FLOAT, INT, OUTPUT,
              INT, INPUT, SWITCH, WHILE, IF, RELOP,
              ADDOP, MULOP, OR, AND, NOT, CAST, ID, NUM}

    ignore = ' \t'

    literals = {'(', ')', '{', '}', ',', ':', ';', '='}

    # tokens lexical expressions
    BREAK = r'break'
    CASE = r'case'
    DEFAULT = r'default'
    ELSE = r'else'
    FLOAT = r'float'
    IF = r'if'
    INPUT = r'input'
    INT = r'int'
    OUTPUT = r'output'
    SWITCH = r'switch'
    WHILE = r'while'
    OR = r'\|\|'
    AND = r'&&'
    NOT = r'!'
    RELOP = r'(==|!=|<|>|<=|>=)'
    ADDOP = r'(\+|-)'

    # casting
    @_(r'(static_cast<int>|static_cast<float>)')
    def CAST(self, t):
        if t.value == 'static_cast<int>':
            t.value = Constants.CAST_INT
        else:
            t.value = Constants.CAST_FLOAT
        return t

    @_(r'[a-zA-Z][a-zA-Z0-9]*')
    def ID(self, t):
        t.value = Expression(Constants.UNKNOWN_TYPE, t.value, t.value)
        return t

    # ints and floats (NUM)
    @_(r'([0-9]+\.[0-9]*|[0-9]+)')
    def NUM(self, t):
        if is_int(t.value):
            t.value = Expression(Constants.INT_TYPE, int(t.value), int(t.value))
        else:
            t.value = Expression(Constants.FLOAT_TYPE, float(t.value), float(t.value))
        return t

    # line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # handling comments
    @_(r'(/\*(.|\n)*?\*/)')
    def ignore_comment(self, t):
        pass

    MULOP = r'(\*|/)'

    # handle errors
    def error(self, t):
        print("Illegal character '%s', line number: " % t.value[0], self.lineno)
        self.index += 1
