from sly import Parser
from CpqLexer import CpqLexer


class CpqParser(Parser):
    tokens = CpqLexer.tokens

    @_('INT',
       'NUM')
    def abb(self, p):
        return p[0]

    @_('ID ":" "=" abb')
    def test(self, p):
        print('abb equals : ', p[3])
        return 'he'

