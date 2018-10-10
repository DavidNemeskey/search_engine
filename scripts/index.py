#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

"""Indexes simple English text documents with no discernible fields."""

from argparse import ArgumentParser
import codecs
import logging
import os
import os.path as op

from whoosh.index import create_in
from whoosh.fields import Schema, ID, TEXT

def files_in_dir(source_dir, encodings):
    """
    Enumerates simple English text files as documents.

    :param source_dir: the directory that contains the source files.
    :param encodings: the list of encodings to try with a file.
    """
    def _files_in_dir(source_dir, dir_path, encodings):
        for f in os.listdir(dir_path):
            path = op.join(dir_path, f)
            if op.isdir(path):
                yield from _files_in_dir(source_dir, path, encodings)
            else:
                for encoding in encodings:
                    try:
                        with open(path, encoding=encoding) as inf:
                            yield {'name': op.relpath(path, source_dir),
                                   'content': inf.read()}
                        logging.debug('Decoded file {} with encoding {}.'.format(
                            path, encoding))
                        break
                    except UnicodeDecodeError:
                        pass
                else:
                    logging.warning('Could not decode file {}'.format(path))

    return _files_in_dir(source_dir, source_dir, encodings)


def index(index_dir, documents):
    if not op.exists(index_dir):
        os.mkdir(index_dir)

    schema = Schema(name=ID(stored=True, unique=True),
                    content=TEXT(lang='en', phrase=True))

    ix = create_in(index_dir, schema)
    writer = ix.writer()
    for document in documents:
        writer.add_document(**document)
    writer.commit()


def parse_arguments():
    parser = ArgumentParser(
        description='Indexes simple English text documents with no '
                    'discernible fields.')
    parser.add_argument('--source', '-s', required=True, dest='source_dir',
                        help='the directory with the files to index.')
    parser.add_argument('--index', '-i', required=True, dest='index_dir',
                        help='the directory to create the index in.')
    parser.add_argument('--encodings', '-e', action='append', default=[],
                        help='adds an encoding to the list of encodings '
                             'checked for each file. It is possible to '
                             'specify this option more than once. utf-8 is '
                             'always checked first, and us-ascii the fallback.')
    parser.add_argument('--log-level', '-L', default='info',
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='the logging level.')

    args = parser.parse_args()
    if args.source_dir == args.index_dir:
        parser.error('The source and index directories must differ.')
    for encoding in args.encodings:
        try:
            codecs.lookup(encoding)
        except LookupError:
            parser.error('No encoding by the name', encoding, 'exists.')
    args.encodings = ['utf-8'] + args.encodings + ['us-ascii']

    return args


def main():
    args = parse_arguments()
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s',
                        level=logging.getLevelName(args.log_level.upper()))
    documents = files_in_dir(args.source_dir, args.encodings)
    index(args.index_dir, documents)


if __name__ == '__main__':
    main()
