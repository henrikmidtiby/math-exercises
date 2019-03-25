from ..exercise_converter.helper.ChangeMultiChoiceMarkup import *
from ..exercise_converter.helper.WidgetRenderer import *
from nose.tools import assert_equal


def test_render_sorting_widget_1():
    input_values = [MultiChoice(nr=1,
                                items=[MultiChoiceItem(text='ja', is_correct_answer='true'),
                                       MultiChoiceItem(text='nej', is_correct_answer='false')],
                                parameters=['randomizeorder', 'selectmultiple'])]
    expected_output = """
    "multi_choice1": {
        "type": "multiple-choice",
        "properties": {
            "choices": [{
                "title": "ja",
                "correct": true
                },{
                "title": "nej",
                "correct": false
                }]
        },
        "name": "multi_choice1"
    }
    """

    wr = WidgetRenderer()
    wr.add_multi_choice_widgets(input_values)
    actual_output = wr.get_rendered_widgets()

    print(expected_output)
    print(actual_output[0].content)
    assert_equal(expected_output, actual_output[0].content)

