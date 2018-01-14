import csv
import pydash
from . import participants

gql = """
    query PR($owner: String!, $repo:String!, $count: Int!, $after: String) { 
      repository(owner: $owner, name:$repo) {
        issues(first:$count, after:$after) {
          edges {
            node {
              id
              number
              author { login }
              title
              publishedAt
              participants(first:10) {
                nodes{ login }
                pageInfo { hasNextPage }
              }
            }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
"""


def all_data(json):
    return map(item, pydash.get(json, 'data.repository.issues.edges'))


def item(json):
    paths = {
        'id': 'node.id',
        'number': 'node.number',
        'title': 'node.title',
        'author': 'node.author.login',
        'published_at': 'node.publishedAt',
        'participants': 'node.participants.nodes',
        'more_participants': 'node.participants.pageInfo.hasNextPage',
    }
    data = { key: pydash.get(json, path) for key, path in paths.items() }
    return participants.json_to_list(data)


def paging(json):
    return pydash.get(json, 'data.repository.issues.pageInfo')


def writer(stream):
    fieldnames = [
        'id',
        'number',
        'title',
        'author',
        'published_at',
        'participants',
        'more_participants',
    ]
    return csv.DictWriter(stream, fieldnames)


def write_items(stream, data):
    return writer(stream).writerows(map(participants.list_to_string, data))


def write_header(stream):
    writer(stream).writeheader()
