import dataclasses
import os
import re
import signal
import subprocess
import importlib
import sys

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
        test_consult_pl = test_pl.with_name("shared_consult_data.pl")
        with open(test_pl) as f:
            used_variables = set()
            for line in f:
                # find all used variables in this test to put them into
                # the `Template` argument of `setof`
                for used_variable in re.findall(r"\b[A-Z]\w*", line):
                    used_variables.add(used_variable)
        run_submission_cmd = cmd_template.render(
            submission_file=SUBMISSIONS_DIRECTORY / (submission_id + ".pl"),
            test_file=test_pl,
            # optional file with initial data for all tests
            shared_consult_data_file=test_consult_pl,
            variables_list="[" + ",".join(used_variables) + "]",
        )
        try:
            process = subprocess.Popen(
                run_submission_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                start_new_session=True,
            )
            process.wait(timeout=EXECUTION_TIMEOUT_VALUE)
            output = process.stdout.read().decode()
        except subprocess.TimeoutExpired:
            output = "Fatal Error: TL"
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        
        test_verdict = perform_test(output, test_ans, test_number)

        # add additional info
        with open(test_pl) as f:
            test_verdict["test_text"] = f.read()
        if test_consult_pl.exists():
            with open(test_consult_pl) as f:
                test_verdict["test_consult_text"] = f.read()
        else:
            test_verdict["test_consult_text"] = "—"
        execution_result.append(test_verdict)
    return execution_result


def parse_output(output_lines):
    output_lines = output_lines.split("\n")
    for line in output_lines:
        if "fatal error" in line.lower():
            return ["exception: " + line]
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
    valid_exts = ['.ans', '.py']
    tests = []
    for test_pl in (TESTS_DIRECTORY / task).glob("test*.pl"):
        test_number = int(test_pl.name.replace("test_", "").replace(".pl", ""))
        
        test_ans = test_pl.with_name(test_pl.name[: -(len(".pl"))] + ".ans")
        test_py = test_pl.with_name(test_pl.name[: -(len(".pl"))] + ".py")

        test_basename = test_pl.name[: -(len(".pl"))]
        for ext in valid_exts:
            test_ans = test_pl.with_name(test_basename + ext)
            if os.path.exists(test_ans):
                tests.append((test_number, test_pl, test_ans))
                break
    return sorted(tests)  # sorted by test_number (int)

def perform_test(output, test_ans, test_number):
    output_lines = parse_output(output)
    
    ext = os.path.splitext(test_ans)[-1].lower()
    if ext == '.ans':
        return test_result_equal(output_lines, test_ans, test_number)
    elif ext == '.py':
        return test_with_script(output_lines, test_ans, test_number)

    return TestResult(
        test_number,
        "IE: Incorrect test configuration, contact system admin.", 
        output_lines, 
        '')


def test_with_script(output_lines, test_ans, test_number):
    test_ans = os.path.splitext(test_ans)[0]
    test_ans = test_ans.replace('/', '.')
    test_ans = str(test_ans)

    test_dir = '/'.join(test_ans.split('.')[:-1])
    test_ans = test_ans.split('.')[-1]

    sys.path.append(test_dir)

    test_module = importlib.import_module(test_ans)
    importlib.reload(test_module) # To load changes in tests during server running
    func = getattr(test_module, 'test_result')
    result = dataclasses.asdict(TestResult(*test_module.test_result(output_lines, test_number)))
    sys.path.remove(test_dir)
    return result


def test_result_equal(output_lines, test_ans, test_number):
    with open(test_ans) as f:
        correct_lines = [line.strip() for line in f]
    test_verdict = dataclasses.asdict(
        get_test_verdict(output_lines, correct_lines, test_number)
    )
    return test_verdict


def get_test_verdict(output_lines, correct_lines, test_number):
    if any("Fatal Error: TL" in line for line in output_lines):
        return TestResult(test_number, "TL", output_lines, correct_lines)
    if any("exception" in line for line in output_lines):
        return TestResult(test_number, "RE", output_lines, correct_lines)
    if len(output_lines) != len(correct_lines):
        return TestResult(
            test_number, "WA: different number or lines", output_lines, correct_lines
        )
    if set(output_lines) == set(correct_lines):
        return TestResult(test_number, "OK", output_lines, correct_lines)
    return TestResult(test_number, "WA: output mismatch", output_lines, correct_lines)
