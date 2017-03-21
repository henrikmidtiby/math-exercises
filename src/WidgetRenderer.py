import jinja2
import collections

RenderedWidget = collections.namedtuple('RenderedWidget', ['nr', 'content'])


def render_sorting_widget(sorting_widget):
    template = """
"sorting_widget{{- sorting_widget.nr -}}": {
  "type": "sorter",
  "properties": {
    "values": [
      [
        {
          "value": "{{- sorting_widget.matches[0].columna -}}"
        },
        {
          "value": "{{- sorting_widget.matches[0].columnb -}}"
        }
      ]{% for match in sorting_widget.matches[1:] %},
      [
        {
          "value": "{{ match.columna }}"
        },
        {
          "value": "{{ match.columnb }}"
        }
      ]{% endfor %}
    ],
    "columnnamea": "{{- sorting_widget.columna -}}",
    "columnnameb": "{{- sorting_widget.columnb -}}"
  },
  "name": "sorting_widget{{- sorting_widget.nr -}}"
}

"""

    t = jinja2.Template(template)
    values = {'sorting_widget': sorting_widget}
    rendered_exercise = t.render(values)
    return rendered_exercise


class WidgetRenderer:
    def __init__(self):
        self.rendered_widgets = []
        self.rendered_widgets_counter = 0

    def add_answerbox_widgets(self, answers):
        answerbox_template = """
    "input{{- answerbox.nr }}": {
      "type": "equation-input",
      "properties": {
        "content": "{{ answerbox.content }}"
      },
      "name": "input{{- answerbox['nr']}}"
    }"""

        for answer in answers:
            t = jinja2.Template(answerbox_template)
            values = {'answerbox': answer}
            rendered_exercise = t.render(values)
            self.rendered_widgets_counter += 1
            self.rendered_widgets.append(RenderedWidget(self.rendered_widgets_counter,
                                                        rendered_exercise))

    def add_hint_widgets(self, hints):
        hint_template = """
    "hint{{- hint.nr }}": {
      "type": "hint",
      "properties": {
        "content": "{{ hint.content }}"
      },
      "name": "hint{{- hint.nr }}"
    }"""

        for hint in hints:
            t = jinja2.Template(hint_template)
            values = {'hint': hint}
            rendered_exercise = t.render(values)
            self.rendered_widgets_counter += 1
            self.rendered_widgets.append(RenderedWidget(self.rendered_widgets_counter,
                                                        rendered_exercise))

    def add_multi_choice_widgets(self, multichoices):
        multichoice_template = """
    "multi_choice{{- multi_choice.nr }}": {
        "type": "multiple-choice",
        "properties": {
            "choices": [{
                "title": "{{ multi_choice.items[0].text }}",
                "correct": {{ multi_choice.items[0].is_correct_answer }}
                }{% for item in multi_choice.items[1:] %},{
                "title": "{{ item.text }}",
                "correct": {{ item.is_correct_answer }}
                }{% endfor %}]
        },
        "name": "multi_choice{{- multi_choice.nr }}"
    }
    """

        for multi_choice in multichoices:
            t = jinja2.Template(multichoice_template)
            values = {'multi_choice': multi_choice}
            rendered_exercise = t.render(values)
            self.rendered_widgets_counter += 1
            self.rendered_widgets.append(RenderedWidget(self.rendered_widgets_counter,
                                                        rendered_exercise))

    def add_sorting_widgets(self, sorting_widgets):
        for sorting_widget in sorting_widgets:
            rendered_exercise = render_sorting_widget(sorting_widget)
            self.rendered_widgets_counter += 1
            self.rendered_widgets.append(RenderedWidget(self.rendered_widgets_counter,
                                                        rendered_exercise))

    def add_answer_matrix_widgets(self, answer_matrices):
        answer_matrix_template = """
    "answermatrix{{- answer_matrix.nr }}": {
      "type": "matrix",
      "properties": {
        "answer": [{% for item in answer_matrix.items %}{% if item.rownr > 1 %},{% endif %}
            [{% for element in item.elements %}{% if element.elementnr > 1 %},{% endif %}{{- '"' + element.content + '"' -}}{% endfor %}]{% endfor %}],
        "height": {{ answer_matrix.number_of_rows }},
        "width": {{ answer_matrix.number_of_columns }}
      },
      "name": "answermatrix{{- answer_matrix.nr }}"
    }"""

        for answer_matrix in answer_matrices:
            t = jinja2.Template(answer_matrix_template)
            values = {'answer_matrix': answer_matrix}
            rendered_exercise = t.render(values)
            self.rendered_widgets_counter += 1
            self.rendered_widgets.append(RenderedWidget(self.rendered_widgets_counter,
                                                        rendered_exercise))

    def get_rendered_widgets(self):
        return self.rendered_widgets
