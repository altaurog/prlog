import argparse
import csv
import sys

import pandas as pd
import matplotlib.pyplot as plt


def main(options):
    data = all_edges(reader(options.input))
    df = pd.DataFrame(data)
    groups = df.groupby('participant').count()['n']
    groups.sort_values(ascending=False).plot.bar(title=options.title)
    plt.show()


def reader(stream):
    return csv.DictReader(stream)


def item_edges(item):
    exclude = set([item['author'], 'mokriya', 'mokriya-bot'])
    participants = set(item['participants'].split()) - exclude
    return ({'n': item['number'], 'participant': p} for p in participants)


def all_edges(rows):
    for item in rows:
        yield from item_edges(item)


def get_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', default='')
    parser.add_argument('input', type=argparse.FileType('r', encoding='UTF-8'))
    return parser.parse_args(args)


def run():
    options = get_options(sys.argv[1:])
    main(options)


if __name__ == '__main__':
    run()
