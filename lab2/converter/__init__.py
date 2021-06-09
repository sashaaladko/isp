from .json_serializer import JsonSerializer
from .pickle_serializer import PickleSerializer
from .yaml_serializer import YamlSerializer
from .toml_serializer import TomlSerializer
from .obj_converter import *

JSON_SERIALIZER = 0
PICKLE_SERIALIZER = 1
TOML_SERIALIZER = 2
YAML_SERIALZIER = 3

SERIALIZERS = [JSON_SERIALIZER, PICKLE_SERIALIZER, TOML_SERIALIZER, YAML_SERIALZIER]

def create_serializer(serializer):
    if serializer == JSON_SERIALIZER:
        return JsonSerializer()
    if serializer == PICKLE_SERIALIZER:
        return PickleSerializer()
    if serializer == TOML_SERIALIZER:
        return TomlSerializer()
    if serializer == YAML_SERIALZIER:
        return YamlSerializer()
    raise TypeError('Wrong constant')

def create_serializer_by_name(name):
    if name == 'json':
        return JsonSerializer()
    if name == 'pickle':
        return PickleSerializer()
    if name == 'toml':
        return TomlSerializer()
    if name == 'yaml':
        return YamlSerializer()
    raise TypeError('Wrong name')