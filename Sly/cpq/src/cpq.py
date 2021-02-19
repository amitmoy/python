import sys
from sly import Lexer, Parser
from CpqLexer import CpqLexer
from CpqParser import CpqParser
from Utilities import Constants, eprint

if len(sys.argv) < 2:
    eprint('Not enough arguments')
    exit(0)

fullInputFileName = sys.argv[1]
expectedEnding = '.' + Constants.INPUT_FILE_ENDING

if not fullInputFileName.endswith(expectedEnding):
    eprint('File should end with ' + expectedEnding)
    exit(0)

inputFileName = fullInputFileName.replace(expectedEnding, '')

try:
    cplString = open(fullInputFileName, 'r').read()
    lexer = CpqLexer()
    parser = CpqParser()
    # parser.parse(lexer.tokenize("as, ss, ddf : int; \n {}"))
    a = parser.parse(lexer.tokenize(cplString))
    print('its a ',a)
except Exception as e:
    eprint('could\'nt find or open the file ' + fullInputFileName + '\n' + str(e))
    sys.exit(0)
