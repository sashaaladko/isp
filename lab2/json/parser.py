from .json_constants import *
from ..obj_converter import *

def parse_array(tokens, flag=''):
    array = []

    t = tokens[0]
    if t == JSON_RIGHTBRACKET:
        if flag == JSON_TUPLE_FLAG:
            return tuple(array), tokens[1:]
        if flag == JSON_SET_FLAG:
            return set(array), tokens[1:]
        return array, tokens[1:]

    while t != JSON_RIGHTBRACKET:
        result, tokens = parse(tokens)
        array.append(result)

        t = tokens[0]
        if t == JSON_RIGHTBRACKET:
            if flag == JSON_TUPLE_FLAG:
                return tuple(array), tokens[1:]            
            if flag == JSON_SET_FLAG:
                return set(array), tokens[1:]            
            return array, tokens[1:]
        elif t != JSON_COMMA:
            raise SyntaxError('Comma expected')
        else:
            tokens = tokens[1:]

    raise SyntaxError('End-of-array bracket expected')

def parse_object(tokens, flag=''):
    obj = {}

    t = tokens[0]
    if t == JSON_RIGHTBRACE:
        return obj, tokens[1:]

    while t != JSON_RIGHTBRACE:
        if len(tokens) > 1 and tokens[0] == JSON_TUPLE_FLAG and tokens[1] == '[':
            key, tokens = parse_array(tokens[2:], JSON_TUPLE_FLAG)
        else:
            key = tokens[0]
            tokens = tokens[1:]
        
        if tokens[0] != JSON_COLON:
            raise SyntaxError('Colon after key in object expected , got: {}'.format(t))

        value, tokens = parse(tokens[1:])

        obj[key] = value

        t = tokens[0]

        if t == JSON_RIGHTBRACE:
            if flag == JSON_DICT_FLAG:
                return obj, tokens[1:]
            else:
                return dict_to_obj(obj), tokens[1:]
        elif t != JSON_COMMA:
            raise SyntaxError('Comma after pair in object expected c, got: {}'.format(t))

        tokens = tokens[1:]

    raise SyntaxError('End-of-object bracket expected')

def parse(tokens, flag=''):
    if tokens[0] in JSON_FLAGS:
        flag = tokens[0]
        tokens = tokens[1:]

    t = tokens[0]

    if t == JSON_LEFTBRACKET:
        return parse_array(tokens[1:], flag)
    elif t == JSON_LEFTBRACE:
        return parse_object(tokens[1:], flag)
    else:
        return t, tokens[1:]