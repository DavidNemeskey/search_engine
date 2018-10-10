# search_engine

Simple user inteface for Whoosh

## Usage

The scripts of this repository require Python 3 to work.

Both the `index.py` and `search.py` scripts have command-line help that can be
activated by the `-h` option.

### Indexing

The `index.py` script indexes simple text files recursively in a directory
structure. The `-e` option can be used to specify text encodings to try with
the files.

An example run:
```bash
python scripts/index.py -s Text/ -i index -e "iso-8859-1" -L debug
```

The full command line interface:
```
usage: index.py [-h] --source SOURCE_DIR --index INDEX_DIR
                [--encodings ENCODINGS]
                [--log-level {debug,info,warning,error,critical}]

Indexes simple English text documents with no discernible fields.

optional arguments:
  -h, --help            show this help message and exit
  --source SOURCE_DIR, -s SOURCE_DIR
                        the directory with the files to index.
  --index INDEX_DIR, -i INDEX_DIR
                        the directory to create the index in.
  --encodings ENCODINGS, -e ENCODINGS
                        adds an encoding to the list of encodings checked for
                        each file. It is possible to specify this option more
                        than once. utf-8 is always checked first, and us-ascii
                        the fallback.
  --log-level {debug,info,warning,error,critical}, -L {debug,info,warning,error,critical}
                        the logging level.
```

### Search

The `search.py` script reads an index and allows the user to query it. The
Whoosh query language is
[described here](https://whoosh.readthedocs.io/en/latest/querylang.html).

When running in batch mode, the `-b` option should be specified.

The full command line interface:
```
usage: search.py [-h] --index INDEX_DIR [--limit LIMIT] [--batch]
                 [--log-level {debug,info,warning,error,critical}]

Searches in an index created by index.py.

optional arguments:
  -h, --help            show this help message and exit
  --index INDEX_DIR, -i INDEX_DIR
                        the index directory.
  --limit LIMIT, -l LIMIT
                        the number of documents to return for a query.
  --batch, -b           activates batch mode, i.e. suppresses the query
                        prompt.
  --log-level {debug,info,warning,error,critical}, -L {debug,info,warning,error,critical}
                        the logging level.
```
