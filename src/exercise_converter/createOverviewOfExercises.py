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
from collections import defaultdict


def count_number_of_exercises_in_file(filename):
    number_of_exercises = 0
    pattern_exercise_begin = re.compile("\\\\begin{exercise}")
    with open(filename) as fh:
        for line in fh:
            res = pattern_exercise_begin.match(line)
            if res:
                number_of_exercises += 1

    return number_of_exercises


def get_name_of_first_exercise_in_file(filename):
    pattern_exercise_name = re.compile("\\\\exercisename{(.*)}")
    with open(filename) as fh:
        for line in fh:
            res = pattern_exercise_name.match(line)
            if res:
                return res.group(1)

    return None


def get_all_sub_paths(filename):
    parts_of_filename = filename.split("/")
    for k in range(len(parts_of_filename) + 1):
        yield parts_of_filename[0:k]


def is_new_path_included_in_the_reference_path(reference_path, new_path):
    if len(reference_path) < len(new_path):
        return False
    for k in range(len(new_path)):
        if reference_path[k] != new_path[k]:
            return False
    return True


def leaf_of_path_prefixed_with_tabs(path, text):
    number_of_indents = len(path) - 1
    return "\t"*number_of_indents + path[-1] + text


def generate_tree_expression(list_of_filenames, number_of_exercises_in_files, names_of_exercises):
    output = ""
    last_path = []
    for filename in list_of_filenames:
        parts_of_filename = filename.split("/")
        for val in get_all_sub_paths(filename):
            if not is_new_path_included_in_the_reference_path(last_path, val):
                current_path_name = "/".join(val)
                number_of_exercises = number_of_exercises_in_files[current_path_name]
                text = " (%d) " % number_of_exercises
                try:
                    text += names_of_exercises[current_path_name]
                except:
                    pass
                output += leaf_of_path_prefixed_with_tabs(val, text)
                output += "\n"
        last_path = parts_of_filename
    return output


def main():
    output_file = open('exerciseOverview.txt', 'w')

    latex_files = list(glob.iglob('**/*.tex', recursive=True))
    latex_files.sort()
    number_of_exercises_in_files = defaultdict(int)
    names_of_exercises_in_files = defaultdict(str)
    for filename in latex_files:
        full_filename = filename
        number_of_exercises = count_number_of_exercises_in_file(full_filename)
        for sub_path in get_all_sub_paths(filename):
            number_of_exercises_in_files["/".join(sub_path)] += number_of_exercises

        exercise_name = get_name_of_first_exercise_in_file(full_filename)
        names_of_exercises_in_files[full_filename] = exercise_name

    exercise_tree = generate_tree_expression(latex_files, number_of_exercises_in_files, names_of_exercises_in_files)
    print(exercise_tree)
    output_file.write(exercise_tree)
    output_file.close()

    pass


main()

