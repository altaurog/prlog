import csv
import pydash
from operator import itemgetter
from . import op

gql = """
    query IssueTimeline($owner: String!, $repo: String!, $count: Int!, $after: String) {
      repository(owner: $owner, name: $repo) {
        issues(first: $count, after: $after) {
          edges {
            node {
              number
              closedAt
              timeline(first: 84) {
                nodes {
                  __typename
                  ... on AssignedEvent {
                    actor { login }
                    user { login }
                    createdAt
                  }
                  ... on UnassignedEvent {
                    actor { login }
                    user { login }
                    createdAt
                  }
                  ... on ClosedEvent {
                    actor { login }
                    createdAt
                  }
                  ... on ReopenedEvent {
                    actor { login }
                    createdAt
                  }
                  # a pr referencing the issue shows up as
                  # CrossReferencedEvent with pr as source
                  ... on CrossReferencedEvent {
                    actor {login}
                    createdAt
                    source { __typename }
                  }
                }
                totalCount
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
    path = 'data.repository.issues.edges'
    issue_nodes = pydash.get(json, path)
    return filter(itemgetter('actor'), pydash.flatten(map(issue, issue_nodes)))

get_issue_data = op.pathgetter('node',
    number='number',
    closed_at='closedAt',
    num_events='timeline.totalCount',
)

def issue(json):
    path = 'node.timeline.nodes'
    event_nodes = pydash.get(json, path)
    return list(map(event(get_issue_data(json)), event_nodes))


get_event_data = op.pathgetter(
    typename='__typename',
    actor='actor.login',
    user='user.login',
    created_at='createdAt',
    source='source.__typename',
)


def event(issue_data):
    return lambda json: pydash.assign(get_event_data(json), issue_data)


def paging(json):
    return pydash.get(json, 'data.repository.issues.pageInfo')


def writer(stream):
    fieldnames = [
        'number',
        'closed_at',
        'num_events',
        'typename',
        'actor',
        'user',
        'created_at',
        'source',
    ]
    return csv.DictWriter(stream, fieldnames)


def write_items(stream, data):
    return writer(stream).writerows(data)


def write_header(stream):
    writer(stream).writeheader()
