import argparse
from config import *
from challenge_yml import ChallengeYml

def args_parser():
    # main parser
    parser = argparse.ArgumentParser(
            description='''\
                dynamically modify the challenge.yml file
            ''',
            epilog='''
                example : %(prog)s update --attr hints -v 'content of a hint ...' ./web/chall-name 
            ''',
            formatter_class=argparse.RawTextHelpFormatter,
            prefix_chars='-',
            conflict_handler='resolve',
        )
    
    # parent parser
    parent_parser = argparse.ArgumentParser( add_help=False )
    parent_parser.add_argument( 
            'path',
            type=str,
            help='the path of the yaml file to modify',
        )
    parent_parser.add_argument(
            '--attr',
            type=str,
            required=True,
            help='name of attribute to take action on',
        )
    parent_parser.add_argument(
            '--sync',
            action='store_true',
            help='update challenge in ctfd',
        )

    # subparser to add update/delete subcommands
    subparser = parser.add_subparsers(
            dest='subcommand', 
            required=True,
        )

    # for update subcomand
    parser_update = subparser.add_parser(
            SUBCOMMAND_UPDATE, 
            help=f'{SUBCOMMAND_UPDATE} an attribute',
            parents=[parent_parser],
        )
    # for delete subcommand
    parser_delete = subparser.add_parser(
            SUBCOMMAND_DELETE, 
            help=f'{SUBCOMMAND_DELETE} an existent attribute',
            parents=[parent_parser],
        )
    
    # add arguments specific to each subcommand
    args_update_parser(parser_update)
    args_delete_parser(parser_delete)

    return parser

def args_update_parser(parser_update):
    # mutually exclusive group for the action to be taken on a nested attribute
    group = parser_update.add_mutually_exclusive_group()
    group.add_argument(
            '--add-item', 
            action='store_const', 
            const=ChallengeYml.add_item, 
            dest='action_on_item', 
            default=ChallengeYml.add_item,
            help=f"add value to the specified list/dict pointed by -i and/or -k"
        )
    group.add_argument(
            '--update-item', 
            action='store_const', 
            const=ChallengeYml.update_item, 
            dest='action_on_item',
            help=f"update the item pointed by -i and/or -k inside list/dict with the new given value"
        )
    group.add_argument(
            '--del-item', 
            action='store_const', 
            const=ChallengeYml.delete_item, 
            dest='action_on_item',
            help=f"delete the item pointed by -i and/or -k inside a list/dict"
        )

    # index argument to point to an item inside a list
    parser_update.add_argument(
            '-i',
            type=int,
            action='append',
            dest='indices',
            help='index to access the wanted item in a list, counting starts from 0',
            default=[],
        )

    # key argument to point to an item inside a dict
    parser_update.add_argument(
            '-k',
            type=str,
            action='append',
            dest='indices',
            help='key to access the wanted item in a dict',
        )

    # new value to be added or to be used to update an old value
    parser_update.add_argument(
            '-v', '--value',
            nargs='?',
            type=str,
            help='the value of the attribute',
        )

    # type of the given value : `key:value` or `string` 
    parser_update.add_argument(
            '--type-val',
            choices=TYPES_VAL,
            help=f'the type of the value, by default {TYPES_VAL[0]}',
            default=TYPES_VAL[0],                        
        )
    
    parser_update.set_defaults(type_elem=None)

def args_delete_parser(parser_delete):
    pass
           
if __name__ == "__main__":
    parser = args_parser()
    args = parser.parse_args()

    print('Here are the args: ', args)