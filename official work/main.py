#!/usr/bin/python3

import config
from challenge_yml import ChallengeYml
from manip_args import args_parser, validate
import sys


def main(args):
    # parse file
    challyml = ChallengeYml(args.path)

    # call update or remove
    match args.action:
        case config.SUBCOMMAND_UPDATE: challyml.update_attr(args.attr, args.type, args.action_on_item, val=args.value)
        case config.SUBCOMMAND_DELETE: challyml.remove_attr(args.attr)

    # write changes
    challyml.update_file()


def chattr():
    # get args
    parser = args_parser()
    args = parser.parse_args()
    print(args)

    # validate
    validate(args)

    # call main
    main(args)
    # confirm the file is still valid


if __name__ == '__main__':
    chattr()
