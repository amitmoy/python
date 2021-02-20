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
        self.varsCount = 0

    ###############################################
    # Parsing Rules
    ###############################################

    @_('declarations stmt_block')
    def program(self, p):
        if self.errors > 0:
            eprint(str(self.errors) + ' errors detected')
        else:
            eprint('file compiled successfully')
        return self.compiledString

    @_('declarations declaration',
       '')
    def declarations(self, p):
        return

    @_('idlist ":" type ";"')
    def declaration(self, p):
        for key in p[0]:
            self.labelsTable[key.val] = p[2]
            key.type = p[2]
        return p[0]

    @_('INT',
       'FLOAT')
    def type(self, p):
        return p[0]

    @_('idlist "," ID')
    def idlist(self, p):
        if p[2] in p[0] or is_in_dict(self.labelsTable, p[2].val):
            eprint(str(p.lineno) + ' : identifier "' + p[2].val + '" is declared too many times')
            self.errors += 1
        else:
            p[2].type = Constants.UNKNOWN_TYPE
            p[0].append(p[2])
        return p[0]

    @_('ID')
    def idlist(self, p):
        return [p[0]]

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
        if is_in_dict(self.labelsTable, p[0].val):
            idtype = self.labelsTable[p[0].val]
            if idtype == Constants.FLOAT_TYPE:
                if p[2].type != Constants.FLOAT_TYPE:
                    newvar = self.new_var()
                    self.gen('RTOI ' + newvar + ' ' + p[2].result)
                    p[2].type = Constants.FLOAT_TYPE
                    p[2].result = newvar
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

            self.gen(command + ' ' + str(p[0].val) + ' ' + str(p[2].result))
        else:
            eprint(str(p.lineno) + ' : cant resolve identifier "' + str(p[0].val) + '"')
            self.errors += 1
            return
        return p[0]

    @_('INPUT "(" ID ")" ";"')
    def input_stmt(self, p):
        if is_in_dict(self.labelsTable, p[2].val):
            # writing code
            if self.labelsTable[p[2].val] == Constants.FLOAT_TYPE:
                command = 'RINP'
            else:
                command = 'IINP'

            self.gen(command + ' ' + p[2].val)

        else:
            eprint(str(p.lineno) + ' : cant resolve identifier "' + p[0] + '"')
            self.errors += 1
        return p[2]

    @_('OUTPUT "(" expression ")" ";"')
    def output_stmt(self, p):
        # writing code
        if p[2].type == Constants.FLOAT_TYPE:
            command = 'RPRT'
        else:
            command = 'IPRT'

        self.gen(command + ' ' + p[2].result)
        return p[2].result

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
        return 'he'

    @_('stmtlist stmt')
    def stmtlist(self, p):
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

    #  ###Expressions###
    @_('expression ADDOP term')
    def expression(self, p):
        if p[0].type != p[2].type:
            if p[0].type == Constants.FLOAT_TYPE:
                newVar = self.new_var()
                self.gen('ITOR ' + newVar + ' ' + p[2].result)
                p[2].type = Constants.FLOAT_TYPE
                p[2].result = newVar
            else:
                newVar = self.new_var()
                self.gen('ITOR ' + newVar + ' ' + p[0].result)
                p[0].type = Constants.FLOAT_TYPE
                p[0].result = newVar
            termtype = Constants.FLOAT_TYPE
        else:
            termtype = p[0].type

        # writing code
        if termtype == Constants.FLOAT_TYPE:
            if p[1] == '+':
                command = 'RADD'
            else:
                command = 'RSUB'
        else:
            if p[1] == '+':
                command = 'IADD'
            else:
                command = 'ISUB'

        resvar = self.new_var()
        self.gen(command + ' ' + resvar + ' ' + p[0].result + ' ' + p[2].result)

        return Expression(termtype, resvar, resvar)

    @_('term')
    def expression(self, p):
        return p[0]

    @_('term MULOP factor')
    def term(self, p):
        if p[0].type != p[2].type:
            if p[0].type == Constants.FLOAT_TYPE:
                newVar = self.new_var()
                self.gen('ITOR ' + newVar + ' ' + p[2].result)
                p[2].type = Constants.FLOAT_TYPE
                p[2].result = newVar
            else:
                newVar = self.new_var()
                self.gen('ITOR ' + newVar + ' ' + p[0].result)
                p[0].type = Constants.FLOAT_TYPE
                p[0].result = newVar
            termtype = Constants.FLOAT_TYPE
        else:
            termtype = p[0].type

            # writing code
        if termtype == Constants.FLOAT_TYPE:
            if p[1] == '*':
                command = 'RMLT'
            else:
                command = 'RDIV'
        else:
            if p[1] == '*':
                command = 'IMLT'
            else:
                command = 'IDIV'

        resvar = self.new_var()
        self.gen(command + ' ' + resvar + ' ' + p[0].result + ' ' + p[2].result)

        return Expression(termtype, resvar, resvar)

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

        if casttype != p[2].type:
            if casttype == Constants.FLOAT_TYPE:
                command = 'ITOR'
            else:
                command = 'RTOI'
            newvar = self.new_var()
            p[2].type = casttype
            self.gen(command + ' ' + newvar + ' ' + p[2].result)
            p[2].result = newvar
        return p[2]

    @_('ID')
    def factor(self, p):
        if is_in_dict(self.labelsTable, p[0].val):
            idtype = self.labelsTable[p[0].val]
        else:
            idtype = Constants.UNKNOWN_TYPE
            eprint(str(p.lineno) + ' : cant resolve identifier "' + p[0].val + '"')
            self.errors += 1
        return Expression(idtype, p[0].val, p[0].result)

    @_('NUM')
    def factor(self, p):
        return p[0]

    #################################################
    # Parsing Functions
    #################################################

    def new_label(self):
        self.labelsCount += 1
        return '$' + str(self.labelsCount) + '$'

    def gen(self, string):
        self.compiledString += string + '\n'

        self.compiledLine += 1

    def new_var(self):
        self.varsCount += 1
        return 'tmp' + str(self.varsCount)
