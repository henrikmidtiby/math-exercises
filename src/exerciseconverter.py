# -*- coding: utf-8 -*-


import re
import jinja2
import codecs
import argparse
import collections
from ChangeMultiChoiceMarkup import *
from ChangeAnswerBoxMarkup import *
from ChangeHintMarkup import *
from ChangeImageMarkup import *
from ChangeAnswerMatrixMarkup import *

raw_template = u"""
{
  "name": "{{ exercisename }}",
  "document": "{{ question }}\\n\\n {% for hint in hints %}\\n\\n[[ref hint{{- hint['nr'] }}]] {% endfor %}",
  "widgets": { {%- for answerbox in answerboxes %}{% if answerbox.nr > 1 %},{% endif %}
    "input{{- answerbox.nr }}": {
      "type": "equation-input",
      "properties": {
        "content": "{{ answerbox.content }}"
      },
      "name": "input{{- answerbox['nr']}}"
    }{% endfor %}{% for hint in hints %},
    "hint{{- hint.nr }}": {
      "type": "hint",
      "properties": {
        "content": "{{ hint.content }}"
      },
      "name": "hint{{- hint.nr }}"
    }{% endfor %}{% for multichoice in multichoices %},
    "multichoice{{- multichoice.nr }}": {
      "type": "hint",
      "properties": {
        "choices": "{% for item in multichoice.items %}{% endfor %}"
      },
      "name": "multichoice{{- multichoice.nr }}"
    }{% endfor %}{% for answer_matrix in answermatrices %},
    "answermatrix{{- answer_matrix.nr }}": {
      "type": "matrix",
      "properties": {
        "answer": [{% for item in answer_matrix.items %}{% if item.rownr > 1 %},{% endif %}
            [{% for element in item.elements %}{% if element.elementnr > 1 %},{% endif %}{{- '"' + element.content + '"' -}}{% endfor %}]{% endfor %}],
        "height": {{ answer_matrix.number_of_rows }},
        "width": {{ answer_matrix.number_of_columns }}
      },
      "name": "answermatrix{{- answer_matrix.nr }}"
    }{% endfor %}
  }
}
"""

# Definition of used data structures.
Exercise = collections.namedtuple('Exercise', ['name', 'content'])


def change_part_of_markup(input_lines):
    """
    This function does the main part of changing latex markup to the markup used for tekvideo.sdu.dk.
    The function does not handle elements (like answer boxes) that are inserted using the reference markup.
    """
    inline_math = re.compile('(.*)\\$(.*)\\$(.*)')
    for line in input_lines:
        res = inline_math.match(line)
        while res:
            line = "%s[[eql %s]]%s\n" % (res.group(1), res.group(2), res.group(3))
            res = inline_math.match(line)
        line = line.replace("\\(", "[[eql ")
        line = line.replace("\\)", "]]")
        line = line.replace("\\[", "[[eq ")
        line = line.replace("\\]", "]]")
        line = line.replace("\\begin{align*}", "[[eq ")
        line = line.replace("\\end{align*}", "]]")
        line = line.replace("\n\t", " ")
        line = line.replace("\t", " ")
        yield line


def get_exercises(input_lines):
    """
    Generator function, that goes through the given input lines and for each exercise environment found,
    yields a named tuple with the name of the exercise and the content of the exercise environment.
    :param input_lines:
    :return:
    """
    storage = []
    exercise_name = "unknown"
    adding_tings_to_storage = False
    start_exercise = re.compile('\\\\begin\\{exercise\\}\\{(.*)\\}')
    end_exercise = re.compile('\\\\end\\{exercise\\}')
    comment_line = re.compile('%.*')

    for line in input_lines:
        if end_exercise.match(line):
            adding_tings_to_storage = False
            yield Exercise(exercise_name, storage)
            storage = [""]
        if adding_tings_to_storage:
            if not comment_line.match(line):
                storage.append(line)
        res = start_exercise.match(line)
        if res:
            exercise_name = res.group(1)
            adding_tings_to_storage = True


def add_extra_backslashes(input_lines):
    for line in input_lines:
        line = line.replace('\\', '\\\\')
        yield line


def render_exercise(exercise):
    answer_box_parser = ChangeAnswerBoxMarkup()
    multi_choice_parser = ChangeMultiChoiceMarkup()
    answer_matrix_parser = ChangeAnswerMatrixMarkup()
    image__parser = ChangeImageMarkup()
    hint_parser = ChangeHintMarkup()

    question = answer_box_parser.generator(exercise.content)
    question = multi_choice_parser.generator(question)
    question = answer_matrix_parser.generator(question)
    question = image__parser.generator(question)
    hint_parser.parser(question)

    question_text = hint_parser.get_question()

    answers = list(answer_box_parser.get_answers())
    multi_choices = list(multi_choice_parser.get_multi_choices())
    answer_matrices = list(answer_matrix_parser.get_answer_matrices())
    hints = list(hint_parser.get_hints())

    values = {}
    values['exercisename'] = exercise.name
    values['question'] = "".join(add_extra_backslashes(question_text)).replace("\n", "\\n")
    values['hints'] = hints
    values['answerboxes'] = answers
    values['multichoices'] = multi_choices
    values['answermatrices'] = answer_matrices

    t = jinja2.Template(raw_template)

    rendered_exercise = t.render(values)
    return rendered_exercise


def render_exercises(exercises):
    rendered_exercises = []
    for exercise in exercises:
        rendered_exercise = render_exercise(exercise)
        rendered_exercises.append(rendered_exercise)
    return rendered_exercises


def write_exercises_to_file(output_file, rendered_exercises):
    output_file.write("[")
    for exercise_number, exercise in enumerate(rendered_exercises):
        if exercise_number > 0:
            output_file.write(",")
        output_file.write(exercise)
    output_file.write("\n]\n\n")


def extract_exercises_from_file(input_filename):
    output_filename = re.sub('\.tex', '.json', input_filename)
    with codecs.open(input_filename, "r", "utf-8") as fh, \
            codecs.open(output_filename, 'w', 'utf-8') as output_file:
        exercises = list(get_exercises(change_part_of_markup(fh)))
        rendered_exercises = render_exercises(exercises)
        write_exercises_to_file(output_file, rendered_exercises)

    print()
    print("found %d exercises" % exercises.__len__())


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
