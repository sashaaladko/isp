from .json_lexer import lex
from .json_parser import parse
from .json_constants import *
from ..obj_converter import *
import inspect

class JsonSerializer:
    
    def loads(self, string):
        tokens = lex(string)

        result = parse(tokens)[0]

        return result

    def dumps(self, obj, is_dict = True):
        if type(obj) == dict:
            string = ''

            if (is_dict):
                string += JSON_DICT_FLAG

            string += '{'
            dict_len = len(obj)

            if dict_len == 0:
                string += '}'

            for i, (key, val) in enumerate(obj.items()):
                if type(key) == str:
                    string += '"{}": {}'.format(key, self.dumps(val, type(val) == dict))
                elif type(key) == tuple:
                    string += '{}: {}'.format(self.dumps(key, type(key) == dict), 
                            self.dumps(val, type(val) == dict))
                else:
                    string += '{}: {}'.format(key, self.dumps(val, type(val) == dict))

                if i < dict_len - 1:
                    string += ', '
                else:
                    string += '}'

            return string
        elif type(obj) == list:
            string = '['
            list_len = len(obj)

            if list_len == 0:
                return string + ']'

            for i, val in enumerate(obj):
                string += self.dumps(val, type(val) == dict)

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
            return JSON_TUPLE_FLAG + self.dumps(list(obj), False)

        if type(obj) == set:
            return JSON_SET_FLAG + self.dumps(list(obj), False)

        return self.dumps(obj_to_dict(obj), False)

    def load(self, fp):
        fp.seek(0)
        string = fp.read()

        return self.loads(string)  

    def dump(self, obj, fp):
        string = self.dumps(obj)

        fp.write(string)
        fp.flush()

    def __str__(self):
        return 'JSON serializer'