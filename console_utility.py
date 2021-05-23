import argparse

from serializer.json_serializer.json_serializer import JsonSerializer
from serializer.pickle_serializer.pickle_serializer import PickleSerializer
from serializer.test.utils import TestCls


def get_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--input-format', metavar='input-format', type=str)
    parser.add_argument('--input-file', metavar='input-file', type=str)
    parser.add_argument('--output-format', metavar='output-format', type=str)
    parser.add_argument('--output-file', metavar='output-file', type=str)
    parser.add_argument('--config', metavar='config', type=str)

    args = parser.parse_args()
    return args

def check_config(args):
    if args.config is None:
        return

    config_params = JsonSerializer().load(args.config)
    args.input_file = config_params['input-file']
    args.input_format = config_params['input-format']
    args.output_file = config_params['output-file']
    args.output_format = config_params['output-format']



def convert(args):
    input_parser = None

    if args.input_format == 'json':
        input_parser = JsonSerializer()
    elif args.input_format == 'pickle':
        input_parser = PickleSerializer()
    else:
        raise SyntaxError('Undefined input format')

    obj = input_parser.load(args.input_file)

    output_parser = None

    if args.output_format == 'json':
        output_parser = JsonSerializer()
    elif args.output_format == 'pickle':
        output_parser = PickleSerializer()
    else:
        raise SyntaxError('Undefined input format')

    output_parser.dump(obj, args.output_file)

"""
if __name__ == '__main__':
    args = get_arguments()
    check_config(args)
    convert(args)
"""
obj = TestCls()

print(JsonSerializer().loads(JsonSerializer().dumps(obj)).static_m())