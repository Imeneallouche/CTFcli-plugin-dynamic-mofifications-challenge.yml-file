#!/usr/bin/python3

import config
from challenge_yml import ChallengeYml
from manip_args import args_parser 
from validate_args import validate
from utils import sync_chall

def chattr(args): 
    # parse file
    challyml = ChallengeYml(args.path)
    
    # call update or remove
    match args.subcommand:
        case config.SUBCOMMAND_UPDATE: challyml.update_attr(args.attr, args.action_on_item, type_elem=args.type_elem, indices=args.indices, val=args.value)
        case config.SUBCOMMAND_DELETE: challyml.remove_attr(args.attr)
    
    # write changes
    challyml.update_file()

    # sync challenge in CTFd
    if args.sync:
        sync_chall(args.path)

def main():
    # get args
    parser = args_parser()
    args = parser.parse_args()

    # validate
    validate(args)
    
    # call main
    chattr(args)

    # TO-DO: confirm the file is still valid

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)