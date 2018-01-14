import csv
import pydash
from . import participants

gql = """
    query PR($owner: String!, $repo:String!, $count: Int!, $after: String) { 
      repository(owner: $owner, name:$repo) {
        pullRequests(first:$count, after:$after, states:[MERGED]) {
          edges {
            node { 
              id
              number
              title
              publishedAt
              mergedAt
              mergeCommit { id }
              author { login }
              participants(first:10) {
                nodes { login }
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


def all_pr_data(json):
    return map(pr_data, pydash.get(json, 'data.repository.pullRequests.edges'))


def pr_data(json):
    paths = {
        'id': 'node.id',
        'number': 'node.number',
        'title': 'node.title',
        'author': 'node.author.login',
        'merge_commit': 'node.mergeCommit.id',
        'merged_at': 'node.mergedAt',
        'published_at': 'node.publishedAt',
        'participants': 'node.participants.nodes',
        'more_participants': 'node.participants.pageInfo.hasNextPage',
    }
    data = { key: pydash.get(json, path) for key, path in paths.items() }
    return participants.json_to_list(data)


def paging(json):
    return pydash.get(json, 'data.repository.pullRequests.pageInfo')


def pr_writer(stream):
    fieldnames = [
        'id',
        'number',
        'title',
        'author',
        'merge_commit',
        'merged_at',
        'published_at',
        'participants',
        'more_participants',
    ]
    return csv.DictWriter(stream, fieldnames)


def write_prs(stream, data):
    return pr_writer(stream).writerows(map(participants.list_to_string, data))


def write_header(stream):
    pr_writer(stream).writeheader()
