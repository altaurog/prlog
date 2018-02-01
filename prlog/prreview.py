import csv
import pydash
from . import op

gql = """
    query PRReview($owner: String!, $repo:String!, $count: Int!, $after: String) { 
      repository(owner: $owner, name:$repo) {
        pullRequests(first:$count, after:$after, states:[MERGED]) {
          edges {
            node { 
              id
              number
              reviews(first: 20) {
                nodes {
                  id
                  author {
                    login
                  }
                  state
                  createdAt
                  submittedAt
                  publishedAt
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
    path = 'data.repository.pullRequests.edges'
    pr_nodes = pydash.get(json, path)
    return pydash.flatten(map(pr, pr_nodes))


get_pr_data = op.pathgetter('node',
    pr_id='id',
    pr_number='number',
    num_reviews='reviews.totalCount',
)


def pr(json):
    path = 'node.reviews.nodes'
    pr_review_nodes = pydash.get(json, path)
    return list(map(review(get_pr_data(json)), pr_review_nodes))


get_review_data = op.pathgetter(
    id='id',
    author='author.login',
    state='state',
    created_at='createdAt',
    submitted_at='submittedAt',
    published_at='publishedAt',
)


def review(pr_data):
    return lambda json: pydash.assign(get_review_data(json), pr_data)


def paging(json):
    return pydash.get(json, 'data.repository.pullRequests.pageInfo')


def writer(stream):
    fieldnames = [
        'pr_id',
        'pr_number',
        'num_reviews',
        'id',
        'author',
        'state',
        'created_at',
        'submitted_at',
        'published_at',
    ]
    return csv.DictWriter(stream, fieldnames)


def write_items(stream, data):
    return writer(stream).writerows(data)


def write_header(stream):
    writer(stream).writeheader()
