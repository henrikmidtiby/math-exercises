#!/usr/bin/env python
#
# extractComments.py - extract comments in pdf files residing in subdirectories.
#
# Tool created for assisting with correction of exam handins at SDU.
# The tool requires pdfminer, which can be downloaded from
# http://www.unixuser.org/~euske/python/pdfminer/
#
# Author: Henrik Skov Midtiby, hemi@mmmi.sdu.dk
# Date: 2014-01-15

# Load dependencies
import re
import glob


def count_number_of_exercises_in_file(filename):
    number_of_exercises = 0
    pattern_exercise_begin = re.compile("\\\\begin{exercise}")
    with open(filename) as fh:
        for line in fh:
            res = pattern_exercise_begin.match(line)
            if res:
                number_of_exercises += 1

    return number_of_exercises


def main():
    output_file = open('exerciseOverview.txt', 'w')

    latex_files = list(glob.iglob('**/*.tex', recursive=True))
    latex_files.sort()
    for filename in latex_files:
        print(filename)
        full_filename = filename
        number_of_exercises = count_number_of_exercises_in_file(full_filename)
        try:
            output_file.write("\t%s - %d\n" % (filename, number_of_exercises))
        except Exception as E:
            print(E)

    output_file.close()

    pass


main()

