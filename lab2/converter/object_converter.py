import inspect
import types

class ObjectBuilder:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def bind_methods(instance):
    methods = dict(inspect.getmembers(instance, inspect.isfunction))

    for method in methods:
        cur_method = methods[method]

        args = list(inspect.signature(cur_method).parameters)
        
        if len(args) > 0 and args[0] == 'self':
            bind_method(instance, cur_method)

def bind_method(instance, func, as_name=None):

    if as_name == None:
        as_name = func.__name__
    
    bound_method = func.__get__(instance, instance.__class__)
    
    setattr(instance, as_name, bound_method)

def dict_to_obj(d):
    if type(d) != dict:
        return d

    top = ObjectBuilder(**d)

    for i, j in d.items():
        setattr(top, i, j)

    bind_methods(top)

    return top

def obj_to_dict(obj):
    if hasattr(obj, "__iter__") and type(obj) != str:
        return type(obj)([v for v in obj])
    elif hasattr(obj, "__dict__") and not callable(obj):
        attributes = [(key, value) 
                    for key, value in inspect.getmembers(obj)
                    if not key.startswith('_') and not callable(value) 
                    and not inspect.ismethod(value)]

        methods = inspect.getmembers(obj, lambda a: inspect.ismethod(a) 
                                    or type(a) == types.LambdaType)

        d = dict(attributes + methods)

        if hasattr(obj, '__class__'):
            d['__class__'] = inspect.getsource(getattr(obj, '__class__')).replace('"', "'")
        
        return d
    else:
        return obj
        
def is_primitive(obj):
    return type(obj) in [int, float, str, bool, type(None)]

def is_object_or_dict(obj):
    return not (type(obj) in [int, float, str, bool, type(None), list, tuple, set]
                or callable(obj) or inspect.isclass(obj))