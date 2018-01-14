import argparse
import sys

import pandas as pd
import matplotlib.pyplot as plt

def main(options):
    df = pd.read_csv(options.input)
    groups = df.groupby(options.groupby).count()['id']
    groups.sort_values(ascending=False).plot.bar(title=options.title)
    plt.show()

def get_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', default='')
    parser.add_argument('-g', '--groupby', default='author')
    parser.add_argument('input', type=argparse.FileType('r', encoding='UTF-8'))
    return parser.parse_args(args)


if __name__ == '__main__':
    options = get_options(sys.argv[1:])
    main(options)
