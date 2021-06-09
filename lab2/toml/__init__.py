from .toml_lexer import lex
from .toml_parser import parse
from .toml_constants import *
from ..obj_converter import *
import inspect

class TomlSerializer:
    
    def loads(self, string):
        tokens = lex(string)

        result = parse(tokens)[0]

        return result

    def dumps(self, obj, is_dict=True, is_list=True, section= ''):
        if type(obj) == dict:
            string = '' if len(section) == 0 else '\n'

            if (is_dict):
                string += TOML_DICT_FLAG + '\n'

            if len(section) > 0:
                string += f'[{section}]\n'

            nested_objects = {}
            
            for i, (key, val) in enumerate(obj.items()):
                if not is_object_or_dict(val):
                    if type(key) == str:
                        string += '"{}" = {}\n'.format(key, self.dumps(val, 
                            is_dict=type(val) == dict))
                    elif type(key) == tuple:
                        string += '{} = {}'.format(self.dumps(key, type(key) == dict, False), 
                                self.dumps(val, type(val) == dict))        
                    else:
                        string += "{} = {}\n".format(key, self.dumps(val, 
                            is_dict=type(val) == dict))
                else:
                    nested_objects[key] = val

            for i, (key, val) in enumerate(nested_objects.items()):
                current_section = ''
                if len(section) > 0:
                    current_section = section + '.'

                if type(key) == str:
                    current_section += f'"{key}"'
                elif type(key) == int or type(key) == float:
                    current_section += f"'{key}'"
                elif type(key) == tuple:
                    current_section += self.dumps(key, is_dict=False, 
                                is_list=False, section=current_section)
                else:
                    current_section += f'{key}'

                result = self.dumps(val, is_dict=type(val) == dict, section=current_section)

                string += f'{result}'

            return string
        elif type(obj) == list:
            is_root = False
            if is_list:
                string = TOML_LIST_FLAG + ' '
            else:
                string = ''

            string += '['
            list_len = len(obj)

            if list_len == 0:
                return string + ']'

            for i, val in enumerate(obj):
                if type(val) == dict:
                    string += '\n'
                string += self.dumps(val, is_dict=type(val) == dict)

                if i < list_len - 1:
                    string += ', '
                else:
                    string += ']'

            return string
        elif callable(obj) or inspect.isclass(obj):
            string = inspect.getsource(obj).replace('"', "'")
            return '"' + string + '"'
        elif type(obj) == str:
            return '"{}"'.format(obj)
        elif type(obj) == bool:
            return 'true' if obj else 'false'
        elif type(obj) == type(None):
            return 'null'
        elif is_primitive(obj):
            return str(obj)

        if type(obj) == tuple:
            return TOML_TUPLE_FLAG + ' ' + self.dumps(list(obj), is_dict=False, is_list=False)

        if type(obj) == set:
            return TOML_SET_FLAG + ' ' + self.dumps(list(obj), is_dict=False, is_list=False)

        return TOML_OBJECT_FLAG + '\n' + self.dumps(obj_to_dict(obj), is_dict=False, section=section)

    def load(self, fp):
        fp.seek(0)
        string = fp.read()

        return self.loads(string)  

    def dump(self, obj, fp):
        string = self.dumps(obj)

        fp.write(string)
        fp.flush()

    def __str__(self):
        return 'TOML serializer'