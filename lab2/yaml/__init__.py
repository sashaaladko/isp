from .yaml_constants import *
from .yaml_lexer import lex
from .yaml_parser import parse
from ..obj_converter import *
import inspect

class YamlSerializer:

    def loads(self, string):
        tokens = lex(string)

        flag = ''

        if (len(tokens) > 1 and tokens[0] in YAML_FLAGS
            and type(tokens[1]) == str and tokens[1].startswith('\n')):
            flag = tokens[0]
            tokens = tokens[2:]

        result = parse(tokens, flag)[0]
        
        return result

    def dumps(self, obj, is_dict=True, indent=0):
        if type(obj) == dict:
            string = ''

            if indent == 0 and is_dict:
                if len(obj) == 0:
                    return YAML_DICT_FLAG + '\n' + '{}\n'
                string += YAML_DICT_FLAG + '\n'

            dict_len = len(obj)

            if dict_len == 0:
                return ' ' * indent + YAML_DICT_FLAG + ' ' + '{}\n'

            for i, (key, val) in enumerate(obj.items()):
                if is_primitive(val):
                    if type(key) == tuple:
                        string += (' ' * indent + '{}: {}').format(self.dumps(obj=key, is_dict=(type(key) == dict), 
                                                            indent=indent).lstrip(), 
                                                            self.dumps(val, is_dict=(type(val) == dict)), indent)
                    else:
                        string += (' ' * indent + '{}: {}').format(key, 
                            self.dumps(val, is_dict=(type(val) == dict)), indent)
                else:
                    if type(val) == dict:
                        if type(key) == tuple:
                            string += (' ' * indent + YAML_DICT_FLAG + ' ' + '{}:\n{}').format(self.dumps(obj=key, is_dict=(type(key) == dict), 
                                                        indent=indent).lstrip(), 
                                                        self.dumps(obj=val, is_dict=(type(val) == dict), indent=indent + 2))
                        else:
                            string += (' ' * indent + YAML_DICT_FLAG + ' ' + '{}:\n{}').format(key, 
                                self.dumps(obj=val, is_dict=(type(val) == dict), indent=indent + 2))
                    elif type(val) == tuple:
                        if type(key) == tuple:
                            string += (' ' * indent + YAML_TUPLE_FLAG + ' ' + '{}:\n{}').format(self.dumps(obj=key, is_dict=(type(key) == dict),
                                                        indent=indent).lstrip(), 
                                                        self.dumps(obj=list(val), is_dict=(type(val) == dict), indent=indent + 2))
                        else:
                            string += (' ' * indent + YAML_TUPLE_FLAG + ' ' + '{}:\n{}').format(key, 
                                self.dumps(obj=list(val), is_dict=(type(val) == dict), indent=indent + 2))
                    elif type(val) == set:
                        if type(key) == tuple:
                            string += (' ' * indent + YAML_SET_FLAG + ' ' + '{}:\n{}').format(self.dumps(obj=key, is_dict=(type(key) == dict),
                                                        indent=indent).lstrip(), 
                                                        self.dumps(obj=list(val), is_dict=(type(val) == dict), indent=indent + 2))
                        else:
                            string += (' ' * indent + YAML_SET_FLAG + ' ' + '{}:\n{}').format(key, 
                                self.dumps(obj=list(val), is_dict=(type(val) == dict), indent=indent + 2))
                    elif type(val) == list:
                        if type(key) == tuple:
                            string += (' ' * indent + '{}:\n{}').format(self.dumps(obj=key, is_dict=(type(key) == dict), 
                                                        indent=indent).lstrip(), 
                                                        self.dumps(obj=val, is_dict=(type(val) == dict), indent=indent))
                        else:
                            string += (' ' * indent + '{}:\n{}').format(key, 
                                self.dumps(obj=val, is_dict=(type(val) == dict), indent=indent))
                    else:
                        if type(key) == tuple:
                            string += (' ' * indent + '{}:\n{}').format(self.dumps(obj=key, is_dict=(type(key) == dict), 
                                                        indent=indent).lstrip(), 
                                self.dumps(obj=val, is_dict=(type(val) == dict), indent=indent + 2))
                        else:
                            string += (' ' * indent + '{}:\n{}').format(key, 
                                self.dumps(obj=val, is_dict=(type(val) == dict), indent=indent + 2))

            return string
        elif type(obj) == list:
            string = ''

            list_len = len(obj)

            if list_len == 0:
                return ' ' * indent + '[]\n'

            for i, val in enumerate(obj):
                if i == 0:
                    if type(val) == dict:
                        string += (' ' * indent + '- ' + YAML_DICT_FLAG + ' {}').format(self.dumps(val, type(val) == dict, indent + 2).lstrip())
                    else:
                        string += (' ' * indent + '- {}').format(self.dumps(val, type(val) == dict, indent + 2).lstrip())
                else:
                    if type(val) == dict:
                        string += (' ' * indent + '- ' + YAML_DICT_FLAG + ' {}').format(self.dumps(val, type(val) == dict, indent + 2).lstrip())
                    else:
                        string += (' ' * indent + '- {}').format(self.dumps(val, type(val) == dict, indent + 2).lstrip())

            return string
        elif callable(obj) or inspect.isclass(obj):
            string = inspect.getsource(obj).replace('"', "'")
            return '"' + string + '"' + '\n'
        elif type(obj) == str:
            return '"{}"'.format(obj) + '\n'
        elif type(obj) == bool:
            return ('true' if obj else 'false') + '\n'
        elif type(obj) == type(None):
            return 'null' + '\n'
        elif is_primitive(obj):
            return str(obj) + '\n'

        if type(obj) == tuple:
            if indent == 0:
                return YAML_TUPLE_FLAG + '\n' + self.dumps(list(obj), False, indent).lstrip()
            return ' ' * indent + YAML_TUPLE_FLAG + ' ' + self.dumps(list(obj), False, indent).lstrip()

        if type(obj) == set:
            if indent == 0:
                return YAML_SET_FLAG + '\n' + self.dumps(list(obj), False, indent).lstrip()
            return ' ' * indent + YAML_SET_FLAG + ' ' + self.dumps(list(obj), False, indent).lstrip()

        return self.dumps(obj_to_dict(obj), False, indent)
    
    def load(self, fp):
        fp.seek(0)
        string = fp.read()

        return self.loads(string)  

    def dump(self, obj, fp):
        string = self.dumps(obj)

        fp.write(string)
        fp.flush()

    def __str__(self):
        return 'YAML serializer'