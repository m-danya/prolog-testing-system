from typing import Optional


def check_for_errors(
    output_lines: list[str], test_number: int, correct_lines: list[str]
) -> Optional[tuple[int, str, list[str], list[str]]]:
    if any("Fatal Error: TL" in line for line in output_lines):
        return test_number, "TL", output_lines, correct_lines
    if any("exception" in line for line in output_lines):
        return test_number, "RE", output_lines, correct_lines
    return None
