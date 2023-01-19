from common import test

correct_lines = ['Result = [[[[1,2,3,4]]]]', 'yes']
color_count = 4
edges = [(1, 2), (1, 3), (1, 4), (2, 3), (4, 2), (3, 4)]

def test_result(output_lines, test_number):
    return test(output_lines, test_number, correct_lines, 4, color_count, edges)
