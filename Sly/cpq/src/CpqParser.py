from sly import Parser
from CpqLexer import CpqLexer
from Utilities import Constants, eprint, is_in_dict, Expression


class CpqParser(Parser):
    tokens = CpqLexer.tokens

    def __init__(self):
        super.__init__(self)
        self.labelsTable = {}

    @_('declarations stmt_block')
    def program(self, p):
        print('prog ended')
        return 'he'

    @_('declarations declaration',
       '')
    def declarations(self, p):
        return

    @_('idlist ":" type ";"')
    def declaration(self, p):
        for key in p[0]:
            p[0][key] = p[2]
        self.labelsTable.update(p[0])
        return

    @_('INT',
       'FLOAT')
    def type(self, p):
        return p[0]

    @_('idlist "," ID')
    def idlist(self, p):
        if is_in_dict(p[0], p[2]):
            eprint("id " + p[2] + ' is declared 2 times')
            # TODO: error handle
        else:
            p[0][p[2]] = Constants.UNKNOWN_TYPE
        return p[0]

    @_('ID')
    def idlist(self, p):
        return {p[0]: Constants.UNKNOWN_TYPE}

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

    @_('"(" expression ")"')
    def factor(self, p):
        return p[1]

    @_('CAST "(" expression ")"')
    def factor(self, p):
        if p[0] == Constants.CAST_INT:
            casttype = Constants.INT_TYPE
        else:
            casttype = Constants.FLOAT_TYPE

        return Expression(casttype, p[2].val)

    @_('ID')
    def factor(self, p):
        if is_in_dict(self.labelsTable, p[0]):
            idtype = self.labelsTable[p[0]]
        else:
            idtype = Constants.UNKNOWN_TYPE

        return Expression(idtype, p[0])

    @_('NUM')
    def factor(self, p):
        return p[0]
