
"""
write a command line tool which:
- shows how you would take some sets of personal data
    - name,
    - address,
    - phone_number

- serialise them/deserialise them in at least 2 formats.
- display it in at least 2 different ways (no need to use a GUI Framework).
- text output/HTML or any other human readable format is fine.

There is no need to support manual data entry - you could manually write a file
in one of your chosen formats to give you your input test data.

Write it in such a way that it would be easy for a developer:
- to add support for additional storage formats
- to query a list of currently supported formats
- to supply an alternative reader/writer for one of the supported formats

This should ideally show Object-Oriented Design and Design Patterns Knowledge,
were not looking for use of advanced Language constructs.

Provide reasonable Unit Test coverage.
"""


import os
import sys
import argparse

_p = os.path.join(os.path.dirname(__file__), "pd")
if _p not in sys.path:
    sys.path.append(_p)
del _p
from pd.controller import Manager

###############################################################################


def parse_args():
    description = """\
Tool to ingest the data stored from a supported file format.
Can render the data to html or to the console.
Can convert the source data to another format.

supports the following formats: {ext}

Examples:
python main.py -q
python main.py -i ../data/personal.xml -r html
python main.py -i ../data/personal.xml -o ../output/personal_out.json
python main.py -i ../data/personal.xml
""".format(ext=Manager.supported_formats())
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "-i", "--infile",
        help=("Path of the source file to read data from (required)"))
    parser.add_argument(
        "-q", "--query",
        action="store_true",
        help=("print supported storage formats"))
    parser.add_argument(
        "-o", "--outfile",
        help=("Path of the destination file to write the data to"))
    parser.add_argument(
        "-r", "--render",
        choices=Manager.supported_renderers(),
        help=("Render the data retrieved from the source file to "))

    args = parser.parse_args()
    # print args

    if args.query:
        print "The following formats are suppored: {0}".format(
            Manager.supported_formats())
        return 0

    if not args.infile:
        print "input filepath [-i] is required"
        return 1
    infile = os.path.abspath(args.infile)
    manager = Manager(infile)
    manager.load_file()
    if args.render:
        manager.render_data(args.render)
    if args.outfile:
        manager.outfile = os.path.abspath(args.outfile)
        manager.convert_source_file()

    return args


def main():
    parse_args()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
