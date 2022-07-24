import yaml


def parse_yaml(pathName):
    with open(pathName) as f:
        parsed_content = yaml.load(f, Loader=yaml.SafeLoader)
        return parsed_content

# .
# .
# .
# .


def generate_yaml(content):
    return yaml.dump(content, Dumper=yaml.SafeDumper)


def write_to_yaml(content, pathname):
    with open(pathname, 'w') as f:
        f.write(generate_yaml(content))

# .
# .
# .
# .


def existAttribute(parsedYaml, attributeName):
    for k, v in parsedYaml.items():
        if (k == attributeName):
            return True
    return False

# .
# .
# .
# .


def update(parsedYaml, attributeName, Type, value, action_on_item):
    if(existAttribute(parsedYaml, attributeName)):
        if(Type != 'Other'):
            if(action_on_item == 1):
                item = addItem(value, Type)
                if(Type == "dict"):
                    parsedYaml[attributeName].update(item)
                else:
                    parsedYaml[attributeName].append(item)
            else:
                print("on work...")
        else:
            print("error, attribute don't accept more than one value")
    else:
        print("attribute will be added\n")
        item = addAttribute(attributeName, Type, value)
        parsedYaml.update(item)
    return parsedYaml


# .
# .
# .
# .


def addAttribute(attributeName, Type, value):
    item = addItem(value, Type)
    if (Type == "list"):
        item = {attributeName: [item]}
    else:
        item = {attributeName: item}
    return item


# .
# .
# .
# .
# .
# .
# .
def addItem(value, Type):
    if(Type == "dict"):
        subKey = value.split(':')[0]
        subValue = ':'.join(value.split(':')[1:])
        value = {subKey: subValue}
    elif(value.isdigit()):
        value = int(value)
    return value

# .
# .
# .
# .
# .
# .
# .


def validate_indices(parsed, indices):
    if len(indices) == 0:
        return
    x = indices[0]
    if type(x) is int:
        if x > len(parsed)-1:
            raise KeyError(f"given index: {x} is too big")
    else:
        if x not in parsed:
            raise KeyError(f"given key: {x} doesn't exist in the file")
        else:
            validate_indices(parsed[x], indices[1:])

# .
# .
# .
# .
# .
# .
# .


def delete_item(parsed, indices):
    validate_indices(parsed, indices)
    if len(indices) == 0:
        return
    x = indices[0]
    if len(indices) == 1:
        del parsed[x]
    else:
        delete_item(parsed[x], indices[1:])

# .
# .
# .
# .
# .
# .
# .


def update_item(parsed, indices, val):
    validate_indices(parsed, indices)
    if len(indices) == 0:
        return
    x = indices[0]
    if len(indices) == 1:
        parsed[x] = val
    else:
        update_item(parsed[x], indices[1:], val)
