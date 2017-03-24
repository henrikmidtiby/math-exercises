import re
import collections


SorterWidget = collections.namedtuple('SorterWidget', ['nr', 'columna', 'columnb', 'matches'])
SorterWidgetMatch = collections.namedtuple('SorterWidgetMatch', ['columna', 'columnb'])


class ChangeSorterMarkup:
    def __init__(self):
        self.detected_sorting_widgets_markups = []

        self.start_environment = re.compile('\\\\begin\\{sortingwidget\\}\\{(.*)\\}\\{(.*)\\}')
        self.end_environment = re.compile('\\\\end\\{sortingwidget\\}')
        self.matching_pair = re.compile('(.*)&(.*)')

        self.current_items = []

    def add_matches(self, line):
        line = line.replace('\\\\\n', '')
        line = line.replace('\\', '\\\\')
        res = self.matching_pair.match(line)

        if res:
            temp = SorterWidgetMatch(res.group(1), res.group(2))
            self.current_items.append(temp)
        else:
            print("Bad markup, '%s'" % line)

    def generator(self, input_lines):
        count = 0
        column_a = None
        column_b = None
        in_sorting_widget_environment = False

        for line in input_lines:
            res_start_environment = self.start_environment.match(line)
            res_end_environment = self.end_environment.match(line)
            if res_end_environment:
                in_sorting_widget_environment = False
                count += 1
                yield "[[ref sorting_widget%d]]\n" % count
                self.detected_sorting_widgets_markups.append(SorterWidget(count, column_a, column_b, self.current_items))
                self.current_items = []
            elif res_start_environment:
                in_sorting_widget_environment = True
                try:
                    column_a = res_start_environment.group(1)
                    column_b = res_start_environment.group(2)
                except Exception as e:
                    print(e)
            elif in_sorting_widget_environment:
                self.add_matches(line)
            else:
                yield line

    def get_sorting_widgets(self):
        for sorting_widget in self.detected_sorting_widgets_markups:
            yield sorting_widget
