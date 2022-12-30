import regex

from settings import SUBMISSIONS_DIRECTORY


def list_translate(s):
    s = "(" + s + ")"
    s = s.replace(".", ",")
    s = s.replace("(", "[").replace(")", "]")
    char_list = list(s)
    last_comma = None
    for i in range(len(char_list) - 1):
        if char_list[i] == ",":
            last_comma = i
        if char_list[i + 1] == "]" and last_comma is not None:
            char_list[last_comma] = "|"
            last_comma = None
    s = "".join(char_list)
    s = s.replace("|nil]", "]")
    if regex.match("\[+nil\]+", s):
        s = s[1:-1]
    s = s.replace("nil", "[]")
    return s


def horn_to_prolog(clause):
    vars_or_lists = []
    clause = replace_spec_symbols(clause)
    parenthesis = regex.findall("\((?:[^()]++|(?R))*+\)", clause)
    for par in parenthesis:
        vars_or_lists.extend(regex.split(",", par[1:-1]))
    vars_or_lists = [var for var in vars_or_lists if len(var) > 0]
    for var in vars_or_lists:
        if "nil" in var or "." in var:
            clause = clause.replace(var, list_translate(var))
    return clause


def replace_spec_symbols(clause, type="HLP"):
    if type == "HLP":
        clause = clause.replace("<-", ":-").replace(";", ".").replace("?", "?-")
    return clause


def translate(submission_id, type="HLP"):
    if type == "HLP":
        filename = SUBMISSIONS_DIRECTORY / (submission_id + ".pl")
        with open(filename, "r+") as horn_file:
            content = horn_file.read()
            lines = regex.findall("[\w\W]+?;", content)
        with open(filename, "w+") as horn_file:
            for clause in lines:
                print(horn_to_prolog(clause), file=horn_file)
