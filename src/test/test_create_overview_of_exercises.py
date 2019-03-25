from ..exercise_converter.createOverviewOfExercises import *


def test_get_all_sub_paths():
    input = "a/b/c"
    output = list(get_all_sub_paths(input))
    expected_output = [[], ["a"], ["a", "b"], ["a", "b", "c"]]
    assert expected_output == output


def test_is_new_path_included_in_the_reference_path_1():
    input_a = ["a"]
    input_b = ["b"]
    assert is_new_path_included_in_the_reference_path(input_a, input_b) == False


def test_is_new_path_included_in_the_reference_path_2():
    input_a = ["a"]
    input_b = ["a"]
    assert is_new_path_included_in_the_reference_path(input_a, input_b) == True


def test_is_new_path_included_in_the_reference_path_3():
    input_a = ["a", "b"]
    input_b = ["a"]
    assert is_new_path_included_in_the_reference_path(input_a, input_b) == True


def test_is_new_path_included_in_the_reference_path_4():
    input_a = ["a", "b"]
    input_b = ["b"]
    assert is_new_path_included_in_the_reference_path(input_a, input_b) == False
