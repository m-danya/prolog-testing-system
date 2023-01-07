from common import test

correct_lines = ['Result = [[[3,2,1,2,1]]]', 'yes']
color_count = 3
edges = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (3, 4), (4, 5)]

def test_result(output_lines, test_number):
    return test(output_lines, test_number, correct_lines, 5, color_count, edges)