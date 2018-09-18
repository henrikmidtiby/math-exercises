import re
import collections


Hint = collections.namedtuple('Hint', ['nr', 'content'])

class BadlyFormattedHint(Exception):
    pass


def remove_empty_lines_from_start_of_storage(storage):
    try:
        while storage[0] == '' or storage[0] == '\n':
            storage = storage[1:]
    except IndexError as e:
        raise BadlyFormattedHint

    return storage


def remove_empty_lines_from_end_of_storage(storage):
    while storage[-1] == '' or storage[-1] == '\n':
        storage = storage[0:-1]
    return storage


def remove_whitespace_from_start_of_lines(storage):
    storage = [line.lstrip() for line in storage]
    return storage


def remove_newlines_at_end_of_lines(storage):
    storage = [line.rstrip('\n') for line in storage]
    return storage


class ChangeHintMarkup:
    def __init__(self):
        self.question = ""
        self.detected_hints = []
        self.hint_matcher = re.compile('\s*\\\\hint')

    def add_hint(self, count, storage):
        try:
            storage = remove_empty_lines_from_start_of_storage(storage)
            storage = remove_empty_lines_from_end_of_storage(storage)
            storage = remove_whitespace_from_start_of_lines(storage)
            storage = remove_newlines_at_end_of_lines(storage)
            lines = "\n".join(storage)
            lines = lines.replace('\\', '\\\\')
            lines = lines.replace("\n", "\\n")
            self.detected_hints.append(Hint(count, lines))
        except BadlyFormattedHint:
            print("The program is having trouble with parsing a hint.")
            print("The issue appears after the following hints:")
            print(self.detected_hints)

    def parser(self, input_lines):
        count = 0
        storage = []

        for line in input_lines:
            if self.hint_matcher.match(line):
                if count == 0:
                    self.question = "".join(storage)
                else:
                    self.add_hint(count, storage)
                count += 1
                storage = []
            else:
                storage.append(line)

        if count == 0:
            raise Exception("No hints found in exercise.")

        self.add_hint(count, storage)

    def get_question(self):
        return self.question

    def get_hints(self):
        for hint in self.detected_hints:
            yield hint
