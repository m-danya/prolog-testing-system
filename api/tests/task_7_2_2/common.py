import re

def test(output_lines, test_number, correct_lines, expected):
    if any("Fatal Error: TL" in line for line in output_lines):
        return test_number, "TL", output_lines, correct_lines
    if any("exception" in line for line in output_lines):
        return test_number, "RE", output_lines, correct_lines

    p = re.compile(r'Result = \[\[\[(.*?)\]\]\]')
    results = p.search(output_lines[0])
    if results is None or results.group(1) is None:
        return test_number, "WA: output mismatch", output_lines, correct_lines
    
    nums = {int(s) for s in results.group(1).split(',')}
    if nums != expected:
        return test_number, "WA: output mismatch", output_lines, correct_lines
    return test_number, "OK", output_lines, correct_lines