import pydash

def json_to_list(data):
    return pydash.clone_with(data, to_list)

def to_list(val, key):
    if key == 'participants':
        return pydash.map_(val, 'login')
    return None

def list_to_string(data):
    return pydash.clone_with(data, to_string)

def to_string(val, key):
    return ' '.join(val) if key == 'participants' else None
