import pydash

def pathgetter(*bases, **paths):
    b = lambda path: '.'.join((bases + (path,)))
    return lambda o: { k: pydash.get(o, b(path)) for k, path in paths.items() }
