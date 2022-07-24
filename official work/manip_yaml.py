import yaml


def parse_yaml(pathname):
    with open(pathname) as f:
        parsed_content = yaml.load(f, Loader=yaml.SafeLoader)
        return parsed_content


class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


def write_yaml(content, pathname):
    with open(pathname, 'w') as yamlfile:
        yaml.dump(content, yamlfile, sort_keys=False, Dumper=Dumper)


def ch_yaml_attr(yaml, attr, val) -> bool:
    pass
