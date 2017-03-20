import re
import collections


MultiChoice = collections.namedtuple('MultiChoice', ['nr', 'items', 'parameters'])
MultiChoiceItem = collections.namedtuple('MultiChoiceItem', ['text', 'is_correct_answer'])


class ChangeMultiChoiceMarkup:
    def __init__(self):
        self.detected_multi_choice_markups = []

        self.start_environment = re.compile('\\\\begin\\{multichoice\\}(\\[(.*)\\])?')
        self.end_environment = re.compile('\\\\end\\{multichoice\\}')
        self.item_true = re.compile('\s*\\\\itemtrue\s*(.*)')
        self.item_false = re.compile('\s*\\\\itemfalse\s*(.*)')

        self.current_items = []

    def add_item_to_current_items(self, line):
        res_true = self.item_true.match(line)
        res_false = self.item_false.match(line)
        if res_true:
            self.current_items.append(MultiChoiceItem(res_true.group(1), "true"))
        elif res_false:
            self.current_items.append(MultiChoiceItem(res_false.group(1), "false"))
        else:
            raise Exception('Bad markup, was expecting line to start with \itemtrue or \itemfalse.')

    def generator(self, input_lines):
        count = 0
        parameters = ""
        in_multi_choice_environment = False

        for line in input_lines:
            res_start_environment = self.start_environment.match(line)
            res_end_environment = self.end_environment.match(line)
            if res_end_environment:
                in_multi_choice_environment = False
                count += 1
                yield "[[ref multi_choice%d]]\n" % count
                self.detected_multi_choice_markups.append(MultiChoice(count, self.current_items, parameters))
                self.current_items = []
            elif res_start_environment:
                in_multi_choice_environment = True
                try:
                    parameters = res_start_environment.group(2).split(", ")
                except AttributeError:
                    parameters = []
            elif in_multi_choice_environment:
                self.add_item_to_current_items(line)
            else:
                yield line

    def get_multi_choices(self):
        for multi_choice in self.detected_multi_choice_markups:
            yield multi_choice
