from sly import Parser
from CpqLexer import CpqLexer


class CpqParser(Parser):
    tokens = CpqLexer.tokens

    @_('declarations stmt_block')
    def program(self, p):
        print(p[0], p[1])
        return 'he'

    @_('declarations declaration',
       '')
    def declarations(self, p):
        return 'he'

    @_('idlist ":" type ";"')
    def declaration(self, p):
        print(p[0], p[1], p[2], p[3])
        return 'he'

    @_('INT',
       'FLOAT')
    def type(self, p):
        print(p[0])
        return 'he'

    @_('idlist "," ID',
       'ID')
    def idlist(self, p):
        print(p[0], p[1])
        return 'he'

    @_('assignment_stmt',
       'input_stmt',
       'output_stmt',
       'if_stmt',
       'while_stmt',
       'switch_stmt',
       'break_stmt',
       'stmt_block')
    def stmt(self, p):
        print(p[0])
        return 'he'

    @_('ID "=" expression ";"')
    def assignment_stmt(self, p):
        print(p[0], p[1], p[2], p[3])
        return 'he'

    @_('INPUT "(" ID ")" ";"')
    def input_stmt(self, p):
        print(p[0], p[1], p[2], p[3], p[4])
        return 'he'

    @_('OUTPUT "(" expression ")" ";"')
    def output_stmt(self, p):
        print(p[0], p[1], p[2], p[3], p[4])
        return 'he'

    @_('IF "(" boolexpr ")" stmt ELSE stmt')
    def if_stmt(self, p):
        print(p[0], p[1], p[2], p[3], p[4], p[5], p[6])
        return 'he'

    @_('WHILE "(" boolexpr ")" stmt')
    def while_stmt(self, p):
        print(p[0], p[1], p[2], p[3], p[4])
        return 'he'

    @_('SWITCH "(" expression ")" "{" caselist DEFAULT ":" stmtlist "}"')
    def switch_stmt(self, p):
        print(p[0], p[1], p[2], p[3], p[4])
        return 'he'

    @_('caselist CASE NUM ":" stmtlist',
       '')
    def caselist(self, p):
        return 'he'

    @_('BREAK ";"')
    def break_stmt(self, p):
        print(p[0], p[1])
        return 'he'

    @_('"{" stmtlist "}"')
    def stmt_block(self, p):
        print(p[0], p[1], p[2])
        return 'he'

    @_('stmtlist stmt',
       '')
    def stmtlist(self, p):
        return 'he'

    @_('boolexpr OR boolterm',
       'boolterm')
    def boolexpr(self, p):
        print(p[0])
        return 'he'

    @_('boolterm AND boolfactor',
       'boolfactor')
    def boolterm(self, p):
        print(p[0])
        return 'he'

    @_('NOT "(" boolexpr ")"',
       'expression RELOP expression')
    def boolfactor(self, p):
        print(p[0], p[1], p[2], p[3], p[4])
        return 'he'

    @_('expression ADDOP term',
       'term')
    def expression(self, p):
        print(p[0])
        return 'he'

    @_('term MULOP factor',
       'factor')
    def term(self, p):
        print(p[0])
        return 'he'

    @_('"(" expression ")"',
       'CAST "(" expression ")"',
       'ID',
       'NUM')
    def factor(self, p):
        print(p[0])
        return 'he'
