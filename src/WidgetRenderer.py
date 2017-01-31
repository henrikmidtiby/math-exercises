import jinja2
import collections

RenderedWidget = collections.namedtuple('RenderedWidget', ['nr', 'content'])


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

    def get_rendered_widgets(self):
        return self.rendered_widgets
