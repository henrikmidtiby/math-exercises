from createOverviewOfExercises import *


def test_get_all_sub_paths():
    input = "a/b/c"
    output = list(get_all_sub_paths(input))
    expected_output = [[], ["a"], ["a", "b"], ["a", "b", "c"]]
    assert expected_output == output