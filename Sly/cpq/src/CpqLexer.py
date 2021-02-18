from sly import Lexer
from Utilities import Constants, Functions
import Utilities


class CpqLexer(Lexer):

    tokens = {BREAK, CASE, DEFAULT, ELSE, FLOAT, INT, OUTPUT,
              INT, INPUT, SWITCH, WHILE, IF, RELOP,
              ADDOP, MULOP, OR, AND, NOT, CAST, ID, NUM, FL}

    ignore = r' \t'

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
            t.value = Constants.CastInt
        else:
            t.value = Constants.CastFloat
        return t

    ID = '[a-zA-Z][a-zA-Z0-9]*'

    # ints and floats (NUM)
    @_(r'([0-9]+\.[0-9]*|[0-9]+)')
    def NUM(self, t):
        if Functions.isInt(t.value):
            t.value = {'type': 'int', 'val': int(t.value)}
        else:
            t.value = {'type': 'float', 'val': float(t.value)}
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


if __name__ == '__main__':
    data = 'break : \n\n   +=-/* ha _aa  */ || as as9a 9 90 z static_cast<int> output 0.99 2.1 11 13.0'
    lexer = CpqLexer()
    print(int('11'))
    for tok in lexer.tokenize(data):
        print(tok)
