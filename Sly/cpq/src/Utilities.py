import sys

###################################
#Classes
###################################


class Constants:
    CAST_INT = 'int_cast'
    CAST_FLOAT = 'float_cast'
    INPUT_FILE_ENDING = 'ou'
    OUTPUT_FILE_ENDING = 'qud'
    UNKNOWN_TYPE = 'unknown'
    INT_TYPE = 'int'
    FLOAT_TYPE = 'float'


class Expression:
    def __init__(self, type, val):
        self.type = type
        self.val = val


def is_int(num):
    try:
        a = int(num)
    except (TypeError, ValueError):
        return False
    else:
        return True


def eprint(error):
    print(error, file=sys.stderr)


def is_in_dict(dictionary, key):
    try:
        a = dictionary[key]
        return True
    except:
        return False
