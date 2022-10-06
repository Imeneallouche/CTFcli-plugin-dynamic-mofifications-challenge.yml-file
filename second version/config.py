from typing import Any


CHALLENGE_YML_REF_DIRECTORY_NAME = 'ref'
CHALLENGE_YML_CTFCLI_REF_FILENAME = 'challenge.yml.ref'
CHALLENGE_YML_CUSTOM_REF_FILENAME = 'challenge.yml.cust'

SUBCOMMAND_UPDATE = 'update'
SUBCOMMAND_DELETE = 'delete'

LIST_ATTR_TYPE = 'list'
DICT_ATTR_TYPE = 'dict'
OTHER_ATTR_TYPE = 'other'

ATTR_TYPES = {
    LIST_ATTR_TYPE: list,
    DICT_ATTR_TYPE: dict,
    OTHER_ATTR_TYPE: Any
}

KEYPAIR_VAL_TYPE = 'keypair'
STRING_VAL_TYPE = 'string'
