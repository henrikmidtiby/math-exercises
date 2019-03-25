import re
import collections


AnswerMatrix = collections.namedtuple('AnswerMatrix', ['nr', 'number_of_rows', 'number_of_columns', 'items'])
AnswerMatrixRow = collections.namedtuple('AnswerMatrixRow', ['rownr', 'nelements', 'elements'])
AnswerMatrixRowElement = collections.namedtuple('AnswerMatrixRowElement', ['elementnr', 'content'])


class ChangeAnswerMatrixMarkup:
    def __init__(self):
        self.detected_answer_matrix_markups = []

        self.start_environment = re.compile('\s*\\\\begin\\{answermatrix\\}(\\[(.*)\\])?')
        self.end_environment = re.compile('\s*\\\\end\\{answermatrix\\}')

        self.number_of_seen_rows = 0
        self.rows = []

    def add_item_to_current_items(self, line):
        elements = line.split("&")
        current_row = []
        element_counter = 0
        for element in elements:
            cleaned_element = element.replace('\n', '').replace('\\\\', '').strip()
            element_counter += 1
            current_row.append(AnswerMatrixRowElement(element_counter, cleaned_element))
        self.number_of_seen_rows += 1

        self.rows.append(AnswerMatrixRow(self.number_of_seen_rows,
                                         len(elements),
                                         current_row))

    def generator(self, input_lines):
        count = 0
        in_answer_matrix_environment = False

        for line in input_lines:
            res_start_environment = self.start_environment.match(line)
            res_end_environment = self.end_environment.match(line)
            if res_end_environment:
                in_answer_matrix_environment = False
                count += 1
                yield "[[ref answermatrix%d]]\n" % count
                self.detected_answer_matrix_markups.append(AnswerMatrix(count,
                                                                        self.number_of_seen_rows,
                                                                        self.rows[0].nelements,
                                                                        self.rows))
                self.rows = []
                self.number_of_seen_rows = 0
            elif res_start_environment:
                in_answer_matrix_environment = True
            elif in_answer_matrix_environment:
                self.add_item_to_current_items(line)
            else:
                yield line

    def get_answer_matrices(self):
        for multi_choice in self.detected_answer_matrix_markups:
            yield multi_choice
