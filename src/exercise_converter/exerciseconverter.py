# -*- coding: utf-8 -*-
import sys
assert sys.version_info >= (3, 0), "The exercise converter requires python3 to run."

import re
import jinja2
import codecs
import argparse
import collections
from helper.exerciseconverterfunctions import extract_exercises_from_file

def main():
    parser = argparse.ArgumentParser(description='Extract exercises from a latex file and convert '
                                                 'it to json for tekvideo.sdu.dk')
    parser.add_argument('filename',
                        type=str,
                        nargs='?',
                        default='exercises.tex',
                        help='Name of latex file with the exercises.')
    args = parser.parse_args()

    print("Extracting exercises from '%s'." % args.filename)
    extract_exercises_from_file(args.filename)


if __name__ == "__main__":
    main()
