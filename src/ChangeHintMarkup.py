import re
import collections


Hint = collections.namedtuple('Hint', ['nr', 'content'])


class ChangeHintMarkup:
    def __init__(self):
        self.question = ""
        self.detected_hints = []
        self.hint_matcher = re.compile('\\\\hint')

    def add_hint(self, count, storage):
        while storage[0] == '' or storage[0] == '\n':
            storage = storage[1:]
        while storage[-1] == '' or storage[-1] == '\n':
            storage = storage[0:-1]
        lines = "\n".join(storage)
        lines = lines.replace('\\', '\\\\')
        lines = lines.replace("\n", "\\n")
        self.detected_hints.append(Hint(count, lines))

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
