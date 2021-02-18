class Constants:
    CastInt = 'int_cast'
    CastFloat = 'float_cast'


class Functions:

    def isInt(num):
        try:
            a = int(num)
        except (TypeError, ValueError):
            return False
        else:
            return True
