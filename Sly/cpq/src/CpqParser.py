from sly import Parser
from CpqLexer import CpqLexer
from Utilities import Constants, eprint, is_in_dict, Expression


class CpqParser(Parser):
    tokens = CpqLexer.tokens

    def __init__(self):
        Parser.__init__(self)
        self.labelsTable = {}
        self.errors = 0
        self.labelsCount = 0
        self.compiledString = ''
        self.compiledLine = 1

    ###############################################
    # Parsing Rules
    ###############################################

    @_('declarations stmt_block')
    def program(self, p):
        if self.errors > 0:
            eprint(str(self.errors) + ' errors detected')
        else:
            eprint('file compiled successfully')
        return p

    @_('declarations declaration',
       '')
    def declarations(self, p):
        return

    @_('idlist ":" type ";"')
    def declaration(self, p):
        for key in p[0]:
            p[0][key] = p[2]
        self.labelsTable.update(p[0])
        return p[0]

    @_('INT',
       'FLOAT')
    def type(self, p):
        return p[0]

    @_('idlist "," ID')
    def idlist(self, p):
        if is_in_dict(p[0], p[2]) or is_in_dict(self.labelsTable, p[2]):
            eprint(str(p.lineno) + ' : identifier "' + p[2] + '" is declared too many times')
            self.errors += 1
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
        return p[0]

    @_('ID "=" expression ";"')
    def assignment_stmt(self, p):
        if is_in_dict(self.labelsTable, p[0]):
            idtype = self.labelsTable[p[0]]
            if idtype == Constants.FLOAT_TYPE:
                p[2].type = Constants.FLOAT_TYPE
            else:
                if p[2].type != idtype:
                    eprint(str(p.lineno) + ' : cant cast float to int')
                    self.errors += 1
                    return
        # writing code
            if idtype == Constants.FLOAT_TYPE:
                command = 'RASN'
            else:
                command = 'IASN'

            self.gen(command + ' ' + p[0].val + ' ' + p[2].result)
        else:
            eprint(str(p.lineno) + ' : cant resolve identifier "' + p[0] + '"')
            self.errors += 1
            return
        return {'id': p[0], 'val': p[2].val, 'type': p[2].type}

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
        if p[2].type != Constants.INT_TYPE:
            eprint(str(p.lineno) + ' : Cant switch on a float type expression')
            self.errors += 1
            return

        return 'he'

    @_('caselist CASE NUM ":" stmtlist')
    def caselist(self, p):
        if p[2].type != Constants.INT_TYPE:
            eprint(str(p.lineno) + ' : Cant case a float type expression')
            self.errors += 1
            return

        return 'he'

    @_('')
    def caselist(self, p):
        return

    @_('BREAK ";"')
    def break_stmt(self, p):
        print(p[0], p[1])
        return 'he'

    @_('"{" stmtlist "}"')
    def stmt_block(self, p):
        print(p[1])
        return 'he'

    @_('stmtlist stmt')
    def stmtlist(self, p):
        p[0].update(p[1])
        return p[0]

    @_('')
    def stmtlist(self, p):
        return {}

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

    @_('expression ADDOP term')
    def expression(self, p):
        if p[0].type != p[2].type:
            if p[0].type == Constants.FLOAT_TYPE:
                # TODO: ITOR p[2].result
                p[2].type = Constants.FLOAT_TYPE
            else:
                # TODO: ITOR p[0].result
                p[0].type = Constants.FLOAT_TYPE
            termtype = Constants.FLOAT_TYPE
        else:
            termtype = p[0].type

        return Expression(termtype, p[1])

    @_('term')
    def expression(self, p):
        return p[0]

    @_('term MULOP factor')
    def term(self, p):
        if p[0].type != p[2].type:
            if p[0].type == Constants.FLOAT_TYPE:
                # TODO: ITOR p[2].result
                p[2].type = Constants.FLOAT_TYPE
            else:
                # TODO: ITOR p[0].result
                p[0].type = Constants.FLOAT_TYPE
            termtype = Constants.FLOAT_TYPE
        else:
            termtype = p[0].type

        return Expression(termtype, p[1])

    @_('factor')
    def term(self, p):
        return p[0]

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
            eprint(str(p.lineno) + ' : cant resolve identifier "' + p[0] + '"')
            self.errors += 1

        return Expression(idtype, p[0])

    @_('NUM')
    def factor(self, p):
        return p[0]

    #################################################
    # Parsing Functions
    #################################################

    def new_label(self):
        self.labelsCount += 1
        return 'L' + str(self.labelsCount)

    def gen(self, string):
        self.compiledString += string + '\n'
        self.compiledLine += 1

    def label(self, label):
        self.gen(label + ':')
