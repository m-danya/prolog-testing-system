from common import test
correct_lines = ['Result = [[[1,3,5]]]', 'yes']
expected = {1, 3, 5}

def test_result(output_lines, test_number):
    return test(output_lines, test_number, correct_lines, expected)
