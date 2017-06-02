# -*- coding: utf-8 -*-


import re
import jinja2
import codecs
import argparse
import collections
from .ChangeMultiChoiceMarkup import *
from .ChangeSorterMarkup import *
from .ChangeAnswerBoxMarkup import *
from .ChangeHintMarkup import *
from .ChangeImageMarkup import *
from .ChangeAnswerMatrixMarkup import *
from .WidgetRenderer import WidgetRenderer

raw_template = u"""
{
  "name": "{{ exercisename }}",
  "document": "{{ question }}\\n\\n {% for hint in hints %}\\n\\n[[ref hint{{- hint['nr'] }}]] {% endfor %}",
  "widgets": { {%- for rendered_widget in rendered_widgets %}{% if rendered_widget.nr > 1 %},{% endif %}{{ rendered_widget.content }}{% endfor %}
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
    for line in input_lines:
        line = convert_inline_math_markup(line)
        line = convert_underline_markup(line)
        line = convert_emphasis_markup(line)
        line = line.replace("\\(", "[[eql ")
        line = line.replace("\\)", "]]")
        line = line.replace("\\[", "[[eq ")
        line = line.replace("\\]", "]]")
        line = line.replace("\\begin{align*}", "[[eq ")
        line = line.replace("\\end{align*}", "]]")
        line = line.replace("\n\t", " ")
        line = line.replace("\t", " ")
        yield line


def convert_inline_math_markup(line):
    inline_math = re.compile('(.*)\\$(.*)\\$(.*)')
    res = inline_math.match(line)
    while res:
        line = "%s[[eql %s]]%s\n" % (res.group(1), res.group(2), res.group(3))
        res = inline_math.match(line)
    return line


def convert_underline_markup(line):
    underline = re.compile(r'(.*)\\underline{(.*)}(.*)')
    res = underline.match(line)
    if res:
        line = "%s**%s**%s" % (res.group(1), res.group(2), res.group(3))
    return line


def convert_emphasis_markup(line):
    emph = re.compile(r'(.*)\\emph{(.*)}(.*)')
    res = emph.match(line)
    if res:
        line = "%s*%s*%s" % (res.group(1), res.group(2), res.group(3))
    return line


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
    start_exercise = re.compile('\\s*\\\\begin\\{exercise\\}\\{(.*)\\}')
    end_exercise = re.compile('\\s*\\\\end\\{exercise\\}')
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
    sorting_widget_parser = ChangeSorterMarkup()
    answer_matrix_parser = ChangeAnswerMatrixMarkup()
    image__parser = ChangeImageMarkup()
    hint_parser = ChangeHintMarkup()

    question = answer_box_parser.generator(exercise.content)
    question = multi_choice_parser.generator(question)
    question = sorting_widget_parser.generator(question)
    question = answer_matrix_parser.generator(question)
    question = image__parser.generator(question)
    hint_parser.parser(question)

    question_text = hint_parser.get_question()

    answers = list(answer_box_parser.get_answers())
    multi_choices = list(multi_choice_parser.get_multi_choices())
    sorting_widgets = list(sorting_widget_parser.get_sorting_widgets())
    answer_matrices = list(answer_matrix_parser.get_answer_matrices())
    hints = list(hint_parser.get_hints())

    widget_renderer = WidgetRenderer()
    widget_renderer.add_answerbox_widgets(answers)
    widget_renderer.add_hint_widgets(hints)
    widget_renderer.add_multi_choice_widgets(multi_choices)
    widget_renderer.add_sorting_widgets(sorting_widgets)
    widget_renderer.add_answer_matrix_widgets(answer_matrices)
    rendered_widgets = widget_renderer.get_rendered_widgets()

    values = {}
    values['exercisename'] = exercise.name
    values['question'] = "".join(add_extra_backslashes(question_text)).replace("\n", "\\n")
    values['rendered_widgets'] = rendered_widgets
    values['hints'] = hints

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
