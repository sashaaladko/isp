from .json_constants import *
import inspect

def lex_string(string):
    result = ''

    if string[0] == JSON_QUOTE:
        string = string[1:]
    else:
        return None, string
    
    for c in string:
        if c == JSON_QUOTE:            
            return result, string[len(result)+1:]
        else:
            result += c
        
    raise SyntaxError('Expected end of string quote')


def lex_number(string):
    result = ''

    number_characters = [str(digit) for digit in range(0, 10)] + ['-', 'e', '.']

    for c in string:
        if c in number_characters:
            result += c
        else:
            break

    rest = string[len(result):]

    try:
        if '.' in result:
            return float(result), rest

        return int(result), rest
    except:
        return None, string

def lex_bool(string):
    string_len = len(string)

    if string_len >= TRUE_LEN and string[:TRUE_LEN] == 'true':
        return True, string[TRUE_LEN:]
    elif string_len >= FALSE_LEN and string[:FALSE_LEN] == 'false':
        return False, string[FALSE_LEN:]

    return None, string

def lex_null(string):
    string_len = len(string)

    if string_len >= NULL_LEN and string[:NULL_LEN] == 'null':
        return True, string[NULL_LEN:]

    return None, string

def lex(string):
    tokens = []

    while len(string):
        result, string = lex_string(string)
        if result is not None:
            try:
                d = {}

                fixed_result = result.strip()

                if fixed_result.startswith('self.'):
                    fixed_result = fixed_result[5:]
                    
                if fixed_result.startswith('@'):
                    while len(fixed_result) > 3 and fixed_result[:3] != 'def':
                        fixed_result = fixed_result[3:]

                if fixed_result.find('class') == -1 and fixed_result.find('def') == -1 and fixed_result.find('lambda') == -1:
                    raise Exception('Wrong class or function')

                exec(fixed_result, d)

                for k in d:
                    if k != '__builtins__':
                        if callable(d[k]) or inspect.isclass(d[k]):
                            tokens.append(d[k])
                            break
                        raise Exception('Wrong class or function')
                continue
            except Exception as e:
                tokens.append(result)
                continue

        result, string = lex_number(string)
        if result is not None:
            tokens.append(result)
            continue

        result, string = lex_bool(string)
        if result is not None:
            tokens.append(result)
            continue

        result, string = lex_null(string)
        if result is not None:
            tokens.append(None)
            continue

        if string[0] in JSON_WHITESPACE:
            string = string[1:]
        elif string[0] in JSON_SYNTAX or string[0] in JSON_FLAGS:
            tokens.append(string[0])
            string = string[1:]
        else:
            raise SyntaxError('Unexpected character: {}'.format(string[0]))

    return tokens