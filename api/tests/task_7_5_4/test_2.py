from common import test

correct_lines = ['Result = [[[[1,2,1,2]]]]', 'yes']
color_count = 2
edges = [(1, 2), (2, 3), (3, 4)]

def test_result(output_lines, test_number):
    return test(output_lines, test_number, correct_lines, 4, color_count, edges)