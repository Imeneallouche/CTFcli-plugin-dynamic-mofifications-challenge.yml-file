import argparse
from pathlib import Path
from config import *
from challenge_yml import ChallengeYml
import os


def args_parser():
    parser = argparse.ArgumentParser(  # prog='cli plugin',
        formatter_class=argparse.RawTextHelpFormatter,
        #usage='use %(prog)s --help or -h for more information',

        description='''\
                                        dynamically modify the challenge.yml file
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

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('path',
                               help='the path of the yml file to modify',
                               type=str,
                               )
    parent_parser.add_argument('--attr',
                               type=str,
                               required=True,
                               help='name of attribute to take action on'
                               )

    subparser = parser.add_subparsers(
        dest='action',
        required=True
    )
    parser_update = subparser.add_parser(
        SUBCOMMAND_UPDATE,
        help=f'{SUBCOMMAND_UPDATE} help',
        parents=[parent_parser]
    )
    parser_delete = subparser.add_parser(
        SUBCOMMAND_DELETE,
        help=f'{SUBCOMMAND_DELETE} help',
        parents=[parent_parser]
    )

    args_update_parser(parser_update)
    args_delete_parser(parser_delete)

    return parser


def args_update_parser(parser_update):
    parser_update.add_argument('-t', '--type',
                               nargs='?',
                               choices=[
                                   LIST_ATTR_TYPE,
                                   DICT_ATTR_TYPE,
                                   OTHER_ATTR_TYPE
                               ],
                               default=OTHER_ATTR_TYPE,
                               help='the type of the attribute')

    parser_update.add_argument('-v', '--value',
                               nargs='?',
                               type=str,
                               help='the value of the attribute',
                               required=True)

    parser_update.add_argument('--type-val',
                               choices=[KEYPAIR_VAL_TYPE, STRING_VAL_TYPE],
                               default=STRING_VAL_TYPE,
                               help='the type of the value if keypair or string, by default string')

    group = parser_update.add_mutually_exclusive_group()
    group.add_argument('--add-item', action='store_const', const=ChallengeYml.add_item,
                       dest='action_on_item', default=ChallengeYml.add_item)
    group.add_argument('--update-item', action='store_const',
                       const=ChallengeYml.update_item, dest='action_on_item')
    group.add_argument('--del-item', action='store_const',
                       const=ChallengeYml.delete_item, dest='action_on_item')

    parser_update.add_argument('-i',
                               action='append',
                               type=int,
                               dest='indices',
                               help='index to access the wanted item in a list')

    parser_update.add_argument('-k',
                               action='append',
                               type=str,
                               dest='indices',
                               help='key to access the wanted item in a dict')


def args_delete_parser(parser_delete):
    pass


def trans_type(type):
    if type in ATTR_TYPES:
        return ATTR_TYPES[type]

    return Any


def validate_attribute(attrName: str, challYamlRef: ChallengeYml):
    if not challYamlRef.exists_attr(attrName):
        raise KeyError(f"The given attribute {attrName} isn't valid")


def validate_type_attribute(attrName: str, attrType, challYamlRef: ChallengeYml):
    correct_type = challYamlRef.type_attr(attrName)
    if ATTR_TYPES[attrType] == correct_type or \
            (correct_type not in (list, dict) and ATTR_TYPES[attrType] == Any):
        return

    raise Exception(f"The given attribute type {attrType} isn't valid")


def validate_path(pathname):
    path = os.path.abspath(pathname)
    if os.path.isdir(path):
        path = os.path.join(path, 'challenge.yml')

    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError('''invalid path given''')

    if not os.path.splitext(path)[1] in ['.yml', '.yaml']:
        raise argparse.ArgumentTypeError(
            '''the file has not the yaml extension''')


def validate_value(value, Type):
    if Type == KEYPAIR_VAL_TYPE:
        if not ':' in value:
            raise argparse.ArgumentTypeError(
                '''expected syntax for --value when type is dict is key:value''')
        splitted_value = value.split(":")
        subKey, subValue = splitted_value[0], splitted_value[1]
        if subValue.isdigit():
            subValue = int(subValue)
        value = {subKey: subValue}
    elif value.isdigit():
        value = int(value)
    return value


def validate_indices_existence_ref(to_inspect, indices):
    if not len(indices):
        return True

    if isinstance(to_inspect, list):
        for i in to_inspect:
            if validate_indices_existence_ref(i, indices[1:]):
                return True
    elif isinstance(to_inspect, dict) and indices[0] in to_inspect:
        return validate_indices_existence_ref(to_inspect[indices[0]], indices[1:])

    raise Exception(
        f"The given index or key is not valid, please verify them ...")


def validate(args):

    # validate path
    validate_path(args.path)

    challyml_ref = ChallengeYml.gen_ref(
        f"ref/{CHALLENGE_YML_CTFCLI_REF_FILENAME}", f"ref/{CHALLENGE_YML_CUSTOM_REF_FILENAME}")
    print(challyml_ref.parsed)
    # validate attribute
    validate_attribute(args.attr, challyml_ref)
    if args.action == SUBCOMMAND_UPDATE:
        # validate attribute type
        validate_type_attribute(args.attr, args.type, challyml_ref)
        if args.type == DICT_ATTR_TYPE and args.action_on_item == ChallengeYml.add_item:
            args.type_val = KEYPAIR_VAL_TYPE

        # validate given value
        args.value = validate_value(args.value, args.type_val)

        # check if indices are correct
        if args.indices != None:
            validate_indices_existence_ref(
                challyml_ref.parsed[args.attr], args.indices)


if __name__ == "__main__":
    parser = args_parser()
    args = parser.parse_args()

    print('\n\n\nhere are the args: ', args)

    # validate_path(args.path)
    #validate_item(args.value, args.type)


# description='''\
# -------------------------------------------------
# |                                               |
# |                   a cli plugin                |
# |       -----------------------------------     |
# |                                               |
# |        this is a cli plugin that aims to      |
# |              dynamically modify the           |
# |                  challenge.yml                |
# |                      file                     |
# |                                               |
# -------------------------------------------------
# ''',
