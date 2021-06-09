from serializer import *
import argparse
import os

parser = argparse.ArgumentParser(description='JSON, YAML, Pickle, TOML converter',
                                 fromfile_prefix_chars='@')

parser.add_argument('-p',
                    '--path',
                    metavar='path',
                    action='store',
                    type=str,
                    required=True,
                    help='The path to the file to convert.')

parser.add_argument('-l',
                    '--language',
                    metavar='language',
                    action='store',
                    choices=['json', 'yaml', 'pickle', 'toml'],
                    type=str,
                    required=True,
                    help='New markup language after convertion.')

args = parser.parse_args()

try:
    path = args.path
    language = args.language

    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    new_file_name, extension = os.path.splitext(path)

    extension = extension[1:]

    if extension not in ['json', 'yaml', 'toml', 'pickle']:
        raise Exception('Invalid file extension.')

    if extension == language:
        raise Exception("Don't need to convert the same format.")

    with open(path, 'r') as source_fp:
        source_serializer = create_serializer_by_name(extension)

        obj = source_serializer.load(fp=source_fp)

    new_file_name += '.' + language 

    with open(new_file_name, 'w') as target_fp:
        target_serializer = create_serializer_by_name(language)

        target_serializer.dump(obj=obj, fp=target_fp)

    print('File was converted successfully!')
except Exception as e:
    print(e)