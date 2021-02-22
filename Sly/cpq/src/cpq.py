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
except Exception as e:
    eprint('could\'nt find or open the file ' + fullInputFileName + '\n' + str(e))
    sys.exit(0)

try:
    lexer = CpqLexer()
    parser = CpqParser()
    a = parser.parse(lexer.tokenize(cplString))
except:
    eprint('Compiling failed')

try:
    f = open(fullInputFileName+'.'+Constants.OUTPUT_FILE_ENDING, 'w')
    f.write(a)
except:
    eprint('Failed to write compiled file')