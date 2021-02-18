from sly import Lexer


class CpqLexer(Lexer):

    tokens = {BREAK, CASE, DEFAULT, ELSE, FLOAT, INT, OUTPUT,
              INT, INPUT, SWITCH, WHILE, IF, RELOP,
              ADDOP, MULOP, OR, AND, NOT, CAST}

    ignore = r' \t'

    literals = {'(', ')', '{', '}', ',', ':', ';', '='}

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
    MULOP = r'(\*|/)'

    # casting
    @_(r'(static_cast<int>|static_cast<float>)')
    def CAST(self, t):
        if t.value == 'static_cast<int>':


    # line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # handling comments
    @_(r'(/\*(.|\n)*?\*/)')
    def ignore_comment(self, t):
        pass

    # handle errors
    def error(self, t):
        print("Illegal character '%s', line number: " % t.value[0], self.lineno)
        self.index += 1


if __name__ == '__main__':
    data = 'break : \n\n   +=-  */ ||output'
    lexer = CpqLexer()
    for tok in lexer.tokenize(data):
        print(tok)
