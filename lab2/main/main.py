from serializer import *

fp = open('file.json', 'r+')

s = JsonSerializer()

obj = {'a': 1, 'b': (5, 1, 'qwe', (False, True))}

new_obj = s.load(fp)

print(obj == new_obj)
print(new_obj)