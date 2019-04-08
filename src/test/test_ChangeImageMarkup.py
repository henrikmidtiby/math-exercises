from ..exercise_converter.helper.exerciseconverterfunctions import *
from nose.tools import assert_equal

def test_change_image_markup_1():
    input_values = "Line 1\n"
    temp = ChangeImageMarkup()
    storage = []
    for line in temp.generator(input_values.split('\n')):
        storage.append(line)

    assert_equal(["Line 1", ""], storage)

