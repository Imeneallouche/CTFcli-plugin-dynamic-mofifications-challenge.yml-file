import yaml, re

class BeautifiedDumper(yaml.SafeDumper):
    def increase_indent(self, *args, **kwargs):
        return super().increase_indent(flow=False, indentless=False)

    def represent_str(dumper, data):
        if '\n' in data:
            norm_data = re.sub('[ ]+\n', '\n', data)
            return dumper.represent_scalar(u'tag:yaml.org,2002:str', norm_data, style='|')
        return super().represent_str(data)

yaml.add_representer(str, BeautifiedDumper.represent_str, Dumper=BeautifiedDumper)

def parse_yaml(pathname):
    with open(pathname) as f:
        return yaml.load(f, Loader=yaml.SafeLoader)

def write_yaml(content, pathname):
    with open(pathname, 'w') as yamlfile:
        yaml.dump(content, yamlfile, sort_keys=False, Dumper=BeautifiedDumper) 