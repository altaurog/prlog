import argparse
import functools
import sys

from . import github, graphql, pr

def main(options):
    client = make_client(options)
    pr.write_header(options.output)
    for page in graphql.page(client, options.page_size, options.max_pages):
        print(page)
        pr.write_prs(options.output, page)


def make_client(options):
    q = functools.partial(
        graphql.execute,
        github.endpoint,
        options.token,
        pr.gql,
        owner=options.owner,
        repo=options.repo
    )
    def request(*args, **kwargs):
        res = q(*args, **kwargs)
        json = res.json()
        return pr.all_pr_data(json), pr.paging(json)
    return request



def get_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', required=True)
    parser.add_argument('-o', '--owner', required=True)
    parser.add_argument('-r', '--repo', required=True)
    parser.add_argument('-p', '--page-size', type=int, default=100)
    parser.add_argument('--max-pages', type=int)
    parser.add_argument(
        '-O',
        '--output',
        type=argparse.FileType('w', encoding='UTF-8'),
        default='-'
    )
    return parser.parse_args(args)


if __name__ == '__main__':
    options = get_options(sys.argv[1:])
    main(options)
