from .yaml_constants import *
from ..obj_converter import *

def parse_array(tokens, flag='', level=1):
    array = []

    main_flag = flag

    current_level = level

    while len(tokens) > 0 and current_level == level and tokens[0] != YAML_COLON:
        if len(tokens) > 0 and tokens[0] in YAML_FLAGS and tokens[1] != YAML_COLON:
            flag = tokens[0]
            tokens = tokens[1:]
        else:
            flag = main_flag

        value, tokens, current_level = parse(tokens, flag, level=current_level)

        array.append(value)

        if len(tokens) > 0 and tokens[0] == '-' and level == current_level + 2:
            tokens = tokens[1:]
            current_level += 2
    
    return array, tokens, current_level

def parse_object(tokens, flag='', level=1):
    obj = {}

    main_flag = flag

    current_level = level

    while len(tokens) > 1 and current_level == level:
        if len(tokens) > 0 and tokens[0] in YAML_FLAGS and tokens[1] != YAML_COLON:
            flag = tokens[0]
            tokens = tokens[1:]
        else:
            flag = main_flag

        if (len(tokens) > 1 and tokens[0] == YAML_TUPLE_FLAG and tokens[1] != YAML_COLON):
            current_level = len(tokens[1]) if tokens[1].startswith('\n') else level

            if tokens[1].startswith('\n'):
                key, tokens, current_level = parse(tokens[2:], level=current_level)
            else:
                key, tokens, current_level = parse(tokens[1:], level=current_level)
            key = tuple(key)
        elif (len(tokens) > 2 and type(tokens[0]) == str and 
                tokens[0].startswith('\n') and tokens[1] == YAML_DASH 
                and flag == YAML_TUPLE_FLAG):
            current_level = len(tokens[0])
            tokens = tokens[1:]
            key, tokens, current_level = parse(tokens, level=current_level)
            key = tuple(key)
            flag = main_flag
        elif tokens[0] == YAML_DASH:
            key, tokens, current_level = parse(tokens, flag, level=current_level)
        else:
            if type(tokens[0]) == str and tokens[0].startswith('\n'):
                current_level = len(tokens[0])
                tokens = tokens[1:]

            key = tokens[0]
        
            if key == [] and flag == YAML_TUPLE_FLAG:
                key = tuple()
                tokens = tokens[1:]
                current_level = len(tokens[0])

            if key == {}:
                value = tokens[0]
                tokens = tokens[1:]

                current_level = len(tokens[0])
                tokens = tokens[1:]

                return value, tokens, current_level
            
            tokens = tokens[1:]

        if tokens[0] == YAML_COLON:
            tokens = tokens[1:]
        else:
            return key, tokens

        if type(tokens[0]) == str and tokens[0].startswith('\n'):
            value, tokens, current_level = parse(tokens[1:], flag, level=len(tokens[0]))
        else:
            value = tokens[0]
            tokens = tokens[1:]
            
            current_level = len(tokens[0])
            tokens = tokens[1:]

        obj[key] = value

    return obj, tokens, current_level

def parse(tokens, flag='', level=1):
    if tokens[0] == '-':
        result = parse_array(tokens[1:], level=level + 2)

        if flag == YAML_TUPLE_FLAG:
            return tuple(result[0]), result[1], result[2]

        if flag == YAML_SET_FLAG:
            return set(result[0]), result[1], result[2]

        return result
    
    if len(tokens) > 1 and type(tokens[1]) == str and tokens[1].startswith('\n') and tokens[0] != YAML_TUPLE_FLAG:
        if flag == YAML_SET_FLAG:
            return set(), tokens[2:], len(tokens[1])
        if flag == YAML_TUPLE_FLAG:
            return tuple(), tokens[2:], len(tokens[1])
        if flag == YAML_DICT_FLAG:
            return dict(), tokens[2:], len(tokens[1])
        return tokens[0], tokens[2:], len(tokens[1])

    result = parse_object(tokens=tokens, level=level)

    if flag == YAML_DICT_FLAG:
        return result

    return dict_to_obj(result[0]), result[1], result[2]