import sys


class Constants:
    CAST_INT = 'int_cast'
    CAST_FLOAT = 'float_cast'
    INPUT_FILE_ENDING = 'ou'
    OUTPUT_FILE_ENDING = 'qud'


def isint(num):
    try:
        a = int(num)
    except (TypeError, ValueError):
        return False
    else:
        return True


def eprint(error):
    print(error, file=sys.stderr)
