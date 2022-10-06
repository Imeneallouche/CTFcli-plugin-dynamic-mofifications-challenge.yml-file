from manip_yaml import parse_yaml, write_yaml
from utils import get_nested


class ChallengeYml:

    def __init__(self, pathname):
        self.pathname = pathname
        self.parsed = self.parse()

    def parse(self):
        return ChallengeYml.parse_file(self.pathname)

    def update_file(self):
        write_yaml(self.parsed, self.pathname)
    
    def add_attr(self, attr, type_attr, val):
        item = {}
        if type_attr is list:
            item = { attr: [ val ] }
        else:
            item = {attr: val}

        self.parsed.update(item)
        
    def update_attr(self, attr, action_on_item, type_elem = None, indices = [], val = None):
        if self.exists_attr(attr):
            if self.type_elem(attr) in (list, dict):
                action_on_item(self, [ attr ] + indices, val = val)
            else:
                self.parsed[attr] = val
        else:
            self.add_attr(attr, type_elem, val)

    def remove_attr(self, attr):
        self.delete_item([ attr ], None)

    def exists_attr(self, attr) -> bool:
        return attr in self.parsed 

    def type_elem(self, attr, indices: list = []):
        pointed_elem = get_nested(self.parsed, [ attr ] + indices)
        return type(pointed_elem)
       
    def add_item(self, access_list: list, val):
        pointed_elem = get_nested(self.parsed, access_list )
        type_pointed_elem = type(pointed_elem)

        if type_pointed_elem is list:
            pointed_elem.append(val)
        elif type_pointed_elem is dict:
            pointed_elem.update(val)
        else:
            raise Exception(f"The given val can't be added to the item that is neither a list nor a dict")
    
    def update_item(self, access_list: list, val):
        pointed_elem = get_nested(self.parsed, access_list[:-1] )
        pointed_elem[ access_list[-1] ] = val

    def delete_item(self, access_list: list, val = None):
        pointed_elem = get_nested(self.parsed, access_list[:-1] )
        del pointed_elem[ access_list[-1] ]
        
    @staticmethod
    def parse_file(pathname):
        return parse_yaml(pathname)

    @classmethod
    def gen_ref(cls, *paths):
        if not len(paths):
            return None

        challyml_ref = cls(paths[0])
        challyml_ref.pathname = None

        for path in paths[1:]:
            challyml_ref.parsed.update(ChallengeYml.parse_file(path))

        return challyml_ref