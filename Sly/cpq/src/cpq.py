import sys
from sly import Lexer, Parser
from Utilities import Constants, eprint

if len(sys.argv) < 2:
    eprint('Not enough arguments')
    exit(0)

fullInputFileName = sys.argv[1]

if not fullInputFileName.endswith('.' + Constants.INPUT_FILE_ENDING):
    eprint('File should end with ' + '".' + Constants.INPUT_FILE_ENDING + '"')
    exit(0)

inputFileName = fullInputFileName.replace('.' + Constants.INPUT_FILE_ENDING, '')

try:
    cplString = open(fullInputFileName, 'r').read()
    print(cplString)
except:
    eprint('could\'nt open find or open the file ' + fullInputFileName)
    sys.exit(0)





