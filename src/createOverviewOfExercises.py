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
import sys
import os
import re
import os
import glob


def count_number_of_exercises_in_file(filename):
    number_of_exercises = 0
    pattern_exercise_begin = re.compile("\\\\begin{exercise}")
    with open(filename) as fh:
        for line in fh:
            res = pattern_exercise_begin.match(line)
            if res:
                number_of_exercises += 1
                print("exercise found: %s" % line[:-1])

    return number_of_exercises


# main function that iterates through all subdirs and analyzes all files in
# each subdir.
# Extracted comments are stored in the file "statistics".
def main():
    pattern_latex_file = re.compile(".*tex$")
    output_file = open('exerciseOverview.txt', 'w')

    for filename in glob.iglob('**/*.tex', recursive=True):
        print(filename)

    sub_directories = get_list_of_subdirectories('./')
    for subdir in sub_directories:
        print("Subdir: %s" % subdir)
        assignment = subdir[2:]
        output_file.write(assignment + "\n")
        temp_dir = subdir + '/'
        files = get_files_in_directory(temp_dir)
        for filename in files:
            if pattern_latex_file.match(filename):
                full_filename = assignment + "/" + filename
                number_of_exercises = count_number_of_exercises_in_file(full_filename)
                try:
                    output_file.write("\t%s - %d\n" % (filename, number_of_exercises))
                except Exception as E:
                    print("Error analyzing file: %s" % full_filename)
                    print(E)

    output_file.close()

    pass


def get_list_of_subdirectories(path):
    dirs = []
    files_in_dir = os.listdir(path)
    for file_in_dir in files_in_dir:
        if os.path.isdir(path + file_in_dir):
            dirs.append(path + file_in_dir)
    dirs.sort()
    return dirs


def get_files_in_directory(path):
    files = []
    files_in_dir = os.listdir(path)
    for file_in_dir in files_in_dir:
        if os.path.isfile(path + file_in_dir):
            files.append(file_in_dir)
    files.sort()
    return files


main()

