import itertools
import requests

def execute(endpoint, token, query, **variables):
    return requests.post(
        endpoint,
        headers={'Authorization': 'bearer ' + token},
        json={'query': query, 'variables': variables},
    )


def page(client, page_size=100, max_pages=None):
    cursor = None
    for i in itertools.count(1):
        data, paging = client(count=page_size, after=cursor)
        yield data
        if not paging['hasNextPage']:
            break
        if max_pages and i >= max_pages:
            break
        cursor = paging['endCursor']
