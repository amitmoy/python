from sly import Lexer


class CpqLexer(Lexer):

    tokens = {BREAK, CASE, DEFAULT, ELSE, FLOAT, INT, OUTPUT,
              INT, INPUT, STATIC_CAST, SWITCH, WHILE, IF}

    ignore = '\t '

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
    STATIC_CAST = r'static_cast'
    SWITCH = r'switch'
    WHILE = r'while'


if __name__ == '__main__':
    data = 'break output'
    lexer = CpqLexer()
    for tok in lexer.tokenize(data):
        print(tok)
