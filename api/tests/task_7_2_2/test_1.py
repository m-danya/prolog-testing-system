from common import test

expected = {1, 3, 5}


def test_result(output_lines, test_number):
    return test(output_lines, test_number, expected)
