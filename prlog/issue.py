import csv
import pydash
from . import op, participants

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


get_issue_data = op.pathgetter('node',
    id='id',
    number='number',
    title='title',
    author='author.login',
    published_at='publishedAt',
    participants='participants.nodes',
    more_participants='participants.pageInfo.hasNextPage',
)


item = lambda json: participants.json_to_list(get_issue_data(json))


def all_data(json):
    return map(item, pydash.get(json, 'data.repository.issues.edges'))


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
