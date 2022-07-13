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


def update(parsedYaml, attributeName, Type, value):
    if(existAttribute(parsedYaml, attributeName)):
        if(Type == "list" or Type == "dict"):
            print("\nhow do you want to update the attribute:\n 1- add an item\n 2-update an item \n 3-delete an item\n")
            option = int(input("option chosen: "))

            while(option < 1 or option > 3):
                option = input("invalid option try another:")

            if(option == 1):
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

def addItem(value, Type):
    if(Type == "dict"):
        subKey = value.split(':')[0]
        subValue = ':'.join(value.split(':')[1:])
        value = {subKey: subValue}
    elif(value.isdigit()):
        value = int(value)
    return value
