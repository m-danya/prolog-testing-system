import re
from testlib.errorcheck import check_for_errors


def build_correct_linse(expected):
    return [f"Result = [[[{','.join(str(expected))}]]]", "yes"]


def test(output_lines, test_number, expected):
    correct_lines = build_correct_linse(expected)
    error = check_for_errors(output_lines, test_number, correct_lines)
    if error:
        return error

    # parsing a string "Result = [[[1,3,5,17]]]"
    p = re.compile(r"Result = \[\[\[(.*?)\]\]\]")
    results = p.search(output_lines[0])
    if results is None or results.group(1) is None:
        return test_number, "WA: output mismatch", output_lines, correct_lines

    # answer is correct if it is a permutation of correct numbers
    nums = {int(s) for s in results.group(1).split(",")}
    if nums != expected:
        return test_number, "WA: output mismatch", output_lines, correct_lines
    return test_number, "OK", output_lines, correct_lines
