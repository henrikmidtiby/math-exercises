import re
import collections


Answer = collections.namedtuple('Answer', ['nr', 'content'])


class ChangeAnswerBoxMarkup:
    def __init__(self):
        self.detected_answer_boxes = []

        self.answer_box = re.compile('(.*)\\\\answerbox\{(.*)\}(.*)')

    def generator(self, input_lines):
        count = 0

        for line in input_lines:
            res_answer_box = self.answer_box.match(line)
            if res_answer_box:
                count += 1
                answer = Answer(count, res_answer_box.group(2).replace('\\', '\\\\'))
                self.detected_answer_boxes.append(answer)
                line = "%s[[ref input%d]]%s\n" % (res_answer_box.group(1), answer.nr, res_answer_box.group(3))
            yield line

    def get_answers(self):
        for answer in self.detected_answer_boxes:
            yield answer
