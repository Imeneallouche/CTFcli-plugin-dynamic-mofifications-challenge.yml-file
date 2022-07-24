from manip_yaml import parse_yaml, write_yaml
import config


class ChallengeYml:

    def __init__(self, pathname):
        self.pathname = pathname
        self.parsed = self.parse()

    def parse(self):
        return ChallengeYml.parse_file(self.pathname)

    def update_file(self):
        write_yaml(self.parsed, self.pathname)

    def add_attr(self, attr, type, val):
        item = {}
        if type == config.LIST_ATTR_TYPE:
            item = {attr: [val]}
        else:
            item = {attr: val}

        self.parsed.update(item)

    def update_attr(self, attr, type, action_on_item, indices=[], val=None):
        if self.exists_attr(attr):
            match type:
                case config.LIST_ATTR_TYPE | config.DICT_ATTR_TYPE:
                    action_on_item(self, attr, type, indices, val=None)
                case config.LIST_ATTR_TYPE | config.DICT_ATTR_TYPE:
                    action_on_item(self, attr, type, indices=indices, val=val)
                case _: self.parsed[attr] = val
        else:
            self.add_attr(attr, type, val)

    def remove_attr(self, attr):
        if self.exists_attr(attr):
            del self.parsed[attr]
        else:
            raise KeyError(f"The given attribute {attr} doesn't exist")

    def exists_attr(self, attr) -> bool:
        for k, v in self.parsed.items():
            if (k == attr):
                return True
        return False

    def type_attr(self, attr):
        return type(self.parsed[attr])

    def add_item(self, attr, type_attr, index, val):
        match type_attr:
            case config.LIST_ATTR_TYPE: self.parsed[attr].append(val)
            case config.DICT_ATTR_TYPE: self.parsed[attr].update(val)

    def validate_indices(self, indices):
        if len(indices) == 0:
            return
        x = indices[0]
        if type(x) is int:
            if x > len(self.parsed)-1:
                raise KeyError(f"given index: {x} is too big")
        else:
            if x not in self.parsed:
                raise KeyError(f"given key: {x} doesn't exist in the file")
            else:
                self.validate_indices(self.parsed[x], indices[1:])

    def delete_item(self, indices):
        self.validate_indices(self, indices)
        if len(indices) == 0:
            return
        x = indices[0]
        if len(indices) == 1:
            del self.parsed[x]
        else:
            self.delete_item(self.parsed[x], indices[1:])

    def update_item(self, indices, val):
        self.validate_indices(self.parsed, indices)
        if len(indices) == 0:
            return
        x = indices[0]
        if len(indices) == 1:
            self.parsed[x] = val
        else:
            self.update_item(self.parsed[x], indices[1:], val)

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

    @staticmethod
    def update_ref_file():
        pass
