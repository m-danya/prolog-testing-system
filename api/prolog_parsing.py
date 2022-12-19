import dataclasses
import os
import re

from settings import *
from dataclasses import dataclass


@dataclass
class TestResult:
    test_number: int
    # OK / RE / WA: output mismatch / WA: different number or lines / ...
    result: str
    output_lines: list[str]
    correct_lines: list[str]


def execute_on_tests(submission_id, task, cmd_template):
    execution_result = []
    for test_number, test_pl, test_ans in get_task_tests(task):
        run_submission_cmd = cmd_template.render(
            submission_file=SUBMISSIONS_DIRECTORY / (submission_id + ".pl"),
            test_file=test_pl,
        )
        output = os.popen(run_submission_cmd).read()
        output_lines = parse_output(output)
        with open(test_ans) as f:
            correct_lines = [line.strip() for line in f]
        execution_result.append(
            dataclasses.asdict(  # because dataclass is not json serializable
                get_test_verdict(output_lines, correct_lines, test_number)
            )
        )
    return execution_result


def parse_output(output_lines):
    output_lines = output_lines.split("\n")
    first_query_idx = next(
        i for i in range(len(output_lines)) if output_lines[i].startswith("|")
    )
    # remove init lines
    output_lines = output_lines[first_query_idx:]
    # remove empty lines and query lines
    meaningful_lines = list(filter(lambda a: a and not a.startswith("|"), output_lines))
    # remove "(1 ms)" in lines where it appears and spaces from both sides
    meaningful_lines = [
        re.sub(r"\(\d+\s*m?s\)\s*", "", line).strip() for line in meaningful_lines
    ]
    return meaningful_lines


def get_task_tests(task):
    tests = []
    for test_pl in (TESTS_DIRECTORY / task).glob("test*.pl"):
        test_number = int(test_pl.name.replace("test_", "").replace(".pl", ""))
        test_ans = test_pl.with_name(test_pl.name[: -(len(".pl"))] + ".ans")
        tests.append((test_number, test_pl, test_ans))
    return sorted(tests)  # sorted by test_number (int)


def get_test_verdict(output_lines, correct_lines, test_number):
    if len(output_lines) != len(correct_lines):
        return TestResult(
            test_number, "WA: different number or lines", output_lines, correct_lines
        )
    if any("exception" in line for line in output_lines):
        return TestResult(test_number, "RE", output_lines, correct_lines)
    if set(output_lines) == set(correct_lines):
        return TestResult(test_number, "OK", output_lines, correct_lines)
    return TestResult(test_number, "WA: output mismatch", output_lines, correct_lines)
