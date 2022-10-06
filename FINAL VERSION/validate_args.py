import argparse
from challenge_yml import ChallengeYml
import os, sys
from config import *
from utils import get_nested

def validate_attribute(attrName: str, challYamlRef: ChallengeYml):
    if not challYamlRef.exists_attr(attrName):
        raise KeyError(f"The given attribute {attrName} isn't valid")

def validate_path(args):
    path = os.path.abspath(args.path)
    if os.path.isdir(path):
        path = os.path.join(path, CHALLENGE_YML_FILENAME)

    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError('''invalid path given''')

    if not os.path.splitext(path)[1] in ['.yml', '.yaml']:
        raise argparse.ArgumentTypeError('''the file has not the yaml extension''')
    
    args.path = path

# returns {key: value} dictionnary if type is key:value
# else it returns same valueCHALLENGE_YML_FILENAME
# it returns int if given value is only digits 
def validate_value(value, Type):
    if Type == KEY_VAL_TYPE:
        if not ':' in value:
            raise argparse.ArgumentTypeError(f'expected syntax for --value when type is {KEY_VAL_TYPE} is key:value')
        
        splitted_value = value.split(":")
        subKey, subValue = splitted_value[0], splitted_value[1]
        if subValue.isdigit():
            subValue = int(subValue)
        value = { subKey: subValue }

    elif value.isdigit():
        value = int(value)

    return value

# checks if given indices are correct and returns type of the most nested element
def validate_indices_existence_ref(to_inspect, indices):
    if not len(indices):
        return type(to_inspect)

    if isinstance(to_inspect, list):
        for i in to_inspect:
            if t := validate_indices_existence_ref(i, indices[1:]):
                return t
    elif isinstance(to_inspect, dict) and indices[0] in to_inspect:
        return validate_indices_existence_ref(to_inspect[indices[0]], indices[1:])

    raise Exception(f"The given indices or keys are not valid, please verify them ...")

def validate(args):

    # validate path
    validate_path(args)

    path_ref = os.path.join(sys.path[0], REF_DIRNAME)
    challyml_ref = ChallengeYml.gen_ref(*map(lambda filename: os.path.join(path_ref,filename), os.listdir(path_ref)))
    # validate attribute
    validate_attribute(args.attr, challyml_ref)

    if args.subcommand == SUBCOMMAND_UPDATE :
        if args.action_on_item != ChallengeYml.delete_item:
            # check if indices are correct and sets type of pointed element on which action is to be taken on
            args.type_elem = validate_indices_existence_ref(challyml_ref.parsed[args.attr], args.indices)
            if args.type_elem == dict and args.action_on_item == ChallengeYml.add_item:
                args.type_val = KEY_VAL_TYPE
        
            # validate given value
            if args.value != None:
                args.value = validate_value(args.value, args.type_val)

        if len(args.indices) != 0:
            get_nested(ChallengeYml(args.path).parsed, [ args.attr ] + args.indices)