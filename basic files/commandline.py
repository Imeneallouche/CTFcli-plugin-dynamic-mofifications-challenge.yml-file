import argparse
from pathlib import Path


def args_parser():
    parser = argparse.ArgumentParser(prog='cli plugin',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     usage='use %(prog)s --help or -h for more information',

                                     description='''\
                                    -------------------------------------------------
                                    |                                               |
                                    |                   a cli plugin                |
                                    |       -----------------------------------     |
                                    |                                               |
                                    |        this is a cli plugin that aims to      |
                                    |              dynamically modify the           |
                                    |                  challenge.yml                |
                                    |                      file                     |
                                    |                                               |
                                    -------------------------------------------------
                                    ''',

                                     epilog='''\
                                    -------------------------------------------------
                                    |                                               |
                                    |         all five arguments are required       |
                                    |       -----------------------------------     |
                                    |                                               |
                                    |               {update,delete}                 |
                                    |               -a --attribute                  |
                                    |               -t --type                       |
                                    |               -v --value                      |
                                    |               -d --path                       |
                                    -------------------------------------------------
                                    ''',
                                     prefix_chars='-',
                                     conflict_handler='resolve')

    parser.add_argument('action',
                        nargs='?',
                        choices=['update', 'delete'],
                        default='update',
                        type=str,
                        help='update/delete an attribute'
                        )

    parser.add_argument('-a', '--attribute',
                        nargs='?',
                        type=str,
                        required=True,
                        help='name of attribute to update / delete'
                        )

    parser.add_argument('-t', '--type',
                        nargs='?',
                        choices=['simple', 'list', 'dict'],
                        default='simple',
                        type=str,
                        help='the type of the value of the attribute')

    parser.add_argument('-v', '--value',
                        type=str,
                        help='the value of the attribute',
                        required=True)

    parser.add_argument('-d', '--path',
                        nargs='?',
                        help='the path of the yml file to modify',
                        type=Path,
                        required=True)
    return parser
#
#
#
#
#
#
#
#
#
#
#
#
#


parser = None
args = None

if __name__ == "__main__":
    parser = args_parser()
    args = parser.parse_args()


print('\n\n\nhere are the args: ', args)


#
#
#
#
#
#
#
#
#
#


def validate_attribute(attributeName):
    print('validating attribute')
    # on work


def validate_path(path):
    if (not(Path(path).is_file())):
        raise argparse.ArgumentTypeError('''\n
                                     -------------------------------------------------
                                    |                                                |
                                    |               error in file path               |
                                    |       -----------------------------------      |
                                    |           the path  doesn't exist              |
                                    |                                                |
                                    -------------------------------------------------
                                    ''')

    if not ((Path(path).suffix == '.yml') or (Path(path).suffix == '.yaml')):
        raise argparse.ArgumentTypeError('''\n
                                     -------------------------------------------------
                                    |                                                |
                                    |               error in file type               |
                                    |       -----------------------------------      |
                                    |        the file has not the type .yml          |
                                    |                                                |
                                    --------------------------------------------------
                                    ''')


def validate_item(value, Type):
    if(Type == "dict"):
        if(not(':' in value)):
            raise argparse.ArgumentTypeError('''\n
                                     -------------------------------------------------
                                    |                                                |
                                    |           error in value syntax input          |
                                    |       -----------------------------------      |
                                    |                                                |
                                    |           type of the attribute value:         |
                                    |                -t --type dict                  |
                                    |                                                |
                                    |         expected syntax for -v --value:        |
                                    |                  key : value                   |
                                    |                                                |
                                    -------------------------------------------------
                                    ''')


validate_path(args.path)
validate_item(args.value, args.type)
