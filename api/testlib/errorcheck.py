from typing import Optional, Tuple, List

def check_for_errors(
    output_lines: List[str],
    test_number: int,
    correct_lines: List[str]) -> Optional[Tuple[int, str, List[str], List[str]]]:
    if any("Fatal Error: TL" in line for line in output_lines):
        return test_number, "TL", output_lines, correct_lines
    if any("exception" in line for line in output_lines):
        return test_number, "RE", output_lines, correct_lines
    return None