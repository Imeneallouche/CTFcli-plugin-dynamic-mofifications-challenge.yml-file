from ctfcli.cli.challenges import Challenge
    
def sync_chall(chall_dir):
    print('Updating the challenge in CTFd')
    Challenge().sync(challenge = chall_dir)

# return pointed element by list of indices and keys in a nested dict/list
def get_nested(elem: dict|list, indices: list):
    if len(indices) == 0:
        return elem
    
    if type(elem) not in (list, dict):
        raise Exception(f"Error: given indices can't be followed, {elem} is neither list or dict")
 
    x = indices[0]
    if type(x) is int and x >= len(elem):
        raise Exception(f"Error: given index {x} is too big")
    elif type(x) is str and x not in elem :
        raise Exception(f"Error: given key {x} doesn't exist in the file")

    return get_nested(elem[x], indices[1:])