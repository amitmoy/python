from sly import Parser
from CpqLexer import CpqLexer
from Utilities import Constants, eprint, is_in_dict, Expression


class CpqParser(Parser):
    tokens = CpqLexer.tokens

    def __init__(self):
        Parser.__init__(self)
        self.labelsTable = {}
        self.addressTable = {}
        self.errors = 0
        self.adressCount = 0
        self.compiledString = ''
        self.compiledLine = 1
        self.varsCount = 0

    ###############################################
    # Parsing Rules
    ###############################################

    @_('declarations stmt_block')
    def program(self, p):
        if self.errors > 0:  # if any errors
            eprint(str(self.errors) + ' errors detected')
        else:
            # replacing the addresses symbols with actual line numbers
            print(self.addressTable)
            for key in self.addressTable:
                self.compiledString = self.compiledString.replace(key, str(self.addressTable[key]))
            self.gen('HALT')
            eprint('file compiled successfully')
            return self.compiledString

        return Constants.FAIL  # if there is any errors

    @_('declarations declaration',
       '')
    def declarations(self, p):
        return

    @_('idlist ":" type ";"')
    def declaration(self, p):
        # insert ids to labelsTable with the right types
        for key in p[0]:
            key.type = p[2]
            self.labelsTable[key.val] = key
        return p[0]

    @_('INT',
       'FLOAT')
    def type(self, p):
        return p[0]

    @_('idlist "," ID')
    def idlist(self, p):
        if p[2] in p[0] or is_in_dict(self.labelsTable, p[2].val):  # if ID is already declared in idlist or labelstable
            eprint(str(p.lineno) + ' : identifier "' + p[2].val + '" is declared too many times')
            self.errors += 1
        else:  # else adds ID to idlist
            p[2].type = Constants.UNKNOWN_TYPE
            p[0].append(p[2])
        return p[0]

    @_('ID')
    def idlist(self, p):
        return [p[0]]  # return single ID list

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

    # TODO: write documentation
    @_('ID "=" expression ";"')
    def assignment_stmt(self, p):
        if is_in_dict(self.labelsTable, p[0].val):
            idtype = self.labelsTable[p[0].val].type
            idvar = self.labelsTable[p[0].val]
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

            self.gen(command + ' ' + str(idvar.result) + ' ' + str(p[2].result))
        else:
            eprint(str(p.lineno) + ' : cant resolve identifier "' + str(p[0].val) + '"')
            self.errors += 1
            return
        return p[0]

    @_('INPUT "(" ID ")" ";"')
    def input_stmt(self, p):
        if is_in_dict(self.labelsTable, p[2].val):
            idVar = self.labelsTable[p[2].val]

            # finding out the right command
            if self.labelsTable[p[2].val].type == Constants.FLOAT_TYPE:
                command = 'RINP'
            else:
                command = 'IINP'

            self.gen(command + ' ' + idVar.result)

        else:  # ID not found on labelsTable
            eprint(str(p.lineno) + ' : cant resolve identifier "' + p[0] + '"')
            self.errors += 1
        return p[2]

    @_('OUTPUT "(" expression ")" ";"')
    def output_stmt(self, p):

        # finding out the right command
        if p[2].type == Constants.FLOAT_TYPE:
            command = 'RPRT'
        else:
            command = 'IPRT'

        self.gen(command + ' ' + p[2].result)
        return p[2].result

    # ###Flow control commands###
    @_('start_if stmt end_if ELSE getlineno stmt getlineno')
    def if_stmt(self, p):
        self.addressTable[p[0]] = p[4]
        self.addressTable[p[2]] = p[6]
        return

    @_('IF "(" boolexpr ")"')
    def start_if(self, p):  # generate boolean code and then adds new jump command with new address
        jumpAddress = self.new_address()

        self.gen('JMPZ ' + jumpAddress + ' ' + p[2])
        return jumpAddress

    @_('')
    def end_if(self, p):  # jump to the end of if
        jumpAddress = self.new_address()

        self.gen('JUMP ' + jumpAddress)
        return jumpAddress

    @_('start_while stmt getlineno')
    def while_stmt(self, p):
        self.gen('JUMP ' + str(p[0]['jumpTo']))
        self.addressTable[p[0]['addressToFill']] = p[2] + 1
        return 'he'

    @_('WHILE getlineno "(" boolexpr ")"')
    def start_while(self, p):
        whileAddress = self.new_address()
        self.gen('JMPZ ' + whileAddress + ' ' + p[3])
        return {'jumpTo': p[1], 'addressToFill': whileAddress}

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

    # ###Statements###
    @_('"{" stmtlist "}"')
    def stmt_block(self, p):
        return p[1]

    @_('stmtlist stmt')
    def stmtlist(self, p):
        return p[0]

    @_('')
    def stmtlist(self, p):
        return {}

    # ###Booleans###
    @_('boolexpr OR boolterm')
    def boolexpr(self, p):
        boolres = self.new_var()
        # if b1+b2 > 0 then b1 = 1 || b2 = 1
        self.gen('IADD ' + boolres + ' ' + p[0] + ' ' + p[2])
        self.gen('IGRT ' + boolres + ' ' + boolres + ' ' + '1')
        return boolres

    @_('boolterm')
    def boolexpr(self, p):
        return p[0]

    @_('boolterm AND boolfactor')
    def boolterm(self, p):
        boolres = self.new_var()
        # if b1*b2 = 1 then b1=b2=1
        self.gen('IMLT ' + boolres + ' ' + p[2] + ' ' + p[0])
        self.gen('IEQL ' + boolres + ' ' + boolres + ' ' + '1')
        return boolres

    @_('boolfactor')
    def boolterm(self, p):
        return p[0]

    @_('NOT "(" boolexpr ")"')
    def boolfactor(self, p):
        resvar = self.new_var()
        self.gen('IEQL ' + resvar + ' ' + p[2] + ' ' + '0')
        return resvar

    @_('expression RELOP expression')
    def boolfactor(self, p):
        # type checking
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
            exptype = Constants.FLOAT_TYPE
        else:
            exptype = p[0].type

        boolres = self.new_var()
        # operation checking
        if exptype == Constants.FLOAT_TYPE:
            if p[1] == '<=' or p[1] == '>=':
                if p[1] == '<=':
                    command = 'RGRT'
                elif p[1] == '>=':
                    command = 'RLSS'
                self.gen(command + ' ' + boolres + ' ' + p[0].result + ' ' + p[2].result)
                self.gen('IEQL ' + boolres + ' ' + boolres + ' ' + '0')
                return boolres

            if p[1] == '==':
                command = 'REQL'
            elif p[1] == '!=':
                command = 'RNQL'
            elif p[1] == '>':
                command = 'RGRT'
            elif p[1] == '<':
                command = 'RLSS'
            self.gen(command + ' ' + boolres + ' ' + p[0].result + ' ' + p[2].result)
            return boolres
        else:
            if p[1] == '<=' or p[1] == '>=':
                if p[1] == '<=':
                    command = 'IGRT'
                elif p[1] == '>=':
                    command = 'ILSS'
                self.gen(command + ' ' + boolres + ' ' + p[0].result + ' ' + p[2].result)
                self.gen('IEQL ' + boolres + ' ' + boolres + ' ' + '0')
                return boolres

            if p[1] == '==':
                command = 'IEQL'
            elif p[1] == '!=':
                command = 'INQL'
            elif p[1] == '>':
                command = 'IGRT'
            elif p[1] == '<':
                command = 'ILSS'
            self.gen(command + ' ' + boolres + ' ' + p[0].result + ' ' + p[2].result)
            return boolres

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
            idvar = self.labelsTable[p[0].val]
        else:
            idtype = Constants.UNKNOWN_TYPE
            eprint(str(p.lineno) + ' : cant resolve identifier "' + p[0].val + '"')
            self.errors += 1
            return
        return idvar

    @_('NUM')
    def factor(self, p):
        return p[0]

    @_('')
    def getlineno(self, p):  # return the line number of compiled string
        return self.compiledLine

    #################################################
    # Parsing Functions
    #################################################

    def new_address(self):
        address = '$' + str(self.adressCount) + '$'
        self.adressCount += 1
        self.addressTable[address] = -1
        return address

    def gen(self, string):
        self.compiledString += string + '\n'

        self.compiledLine += 1

    def new_var(self):
        self.varsCount += 1
        return 'tmp' + str(self.varsCount)
