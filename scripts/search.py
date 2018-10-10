#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

"""Searches in an index created by Whoosh."""

from argparse import ArgumentParser
import logging
import sys

from whoosh.index import open_dir, EmptyIndexError
from whoosh.qparser import QueryParser


def parse_arguments():
    parser = ArgumentParser(
        description='Searches in an index created by index.py.')
    parser.add_argument('--index', '-i', required=True, dest='index_dir',
                        help='the index directory.')
    parser.add_argument('--limit', '-l', default=10,
                        help='the number of documents to return for a query.')
    parser.add_argument('--batch', '-b', action='store_true',
                        help='activates batch mode, i.e. suppresses the '
                             'query prompt.')
    parser.add_argument('--log-level', '-L', default='info',
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='the logging level.')
    return parser.parse_args()


def main():
    args = parse_arguments()
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s',
                        level=logging.getLevelName(args.log_level.upper()))

    try:
        ix = open_dir(args.index_dir)
        logging.info('Index read from {}.'.format(args.index_dir))
    except EmptyIndexError:
        logging.critical('Could not read index in {}.'.format(args.index_dir))
        sys.exit(1)

    qp = QueryParser('content', schema=ix.schema)
    prompt = 'Query: ' if not args.batch else ''
    with ix.searcher() as searcher:
        while True:
            try:
                query_str = input(prompt)
            except (EOFError, KeyboardInterrupt):
                print()
                break
            query = qp.parse(query_str)

            results = searcher.search(query, limit=args.limit)
            for result in results:
                print(result['name'], result.score, sep='\t')
            print()


if __name__ == '__main__':
    main()
