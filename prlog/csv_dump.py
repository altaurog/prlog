import argparse
import functools
import sys

from . import github, graphql, pr, issue

def main(options):
    client = make_client(options)
    options.query.write_header(options.output)
    for page in graphql.page(client, options.page_size, options.max_pages):
        options.query.write_items(options.output, page)


def make_client(options):
    q = functools.partial(
        graphql.execute,
        github.endpoint,
        options.token,
        options.query.gql,
        owner=options.owner,
        repo=options.repo
    )
    def request(*args, **kwargs):
        res = q(*args, **kwargs)
        json = res.json()
        return options.query.all_data(json), options.query.paging(json)
    return request


modules = {m.__name__.split('.')[-1]: m for m in [pr, issue]}


def get_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', required=True)
    parser.add_argument('-o', '--owner', required=True)
    parser.add_argument('-r', '--repo', required=True)
    parser.add_argument('-p', '--page-size', type=int, default=100)
    parser.add_argument('--max-pages', type=int)
    parser.add_argument(
        '-q',
        '--query',
        type=lambda m: modules[m],
        default='pr',
        choices=list(modules.values()),
    )
    parser.add_argument(
        '-O',
        '--output',
        type=argparse.FileType('w', encoding='UTF-8'),
        default='-',
    )
    return parser.parse_args(args)


def run():
    options = get_options(sys.argv[1:])
    main(options)


if __name__ == '__main__':
    run()
