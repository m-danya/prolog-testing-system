import regex

from settings import SUBMISSIONS_DIRECTORY


def list_translate(s):
    s = "(" + s + ")"
    s = s.replace(".nil)", ")")
    if regex.match("\(+nil\)+", s):
        s = s[1:-1]
    s = s.replace("nil", "()")
    s = s.replace(".", ",")
    s = s.replace("(", "[").replace(")", "]")
    char_list = list(s)
    last_comma = None
    for i in range(len(char_list) - 1):
        if char_list[i] == ",":
            if char_list[i + 1].isupper():
                last_comma = i
            else:
                last_comma = None
        if char_list[i + 1] == "]" and last_comma is not None:
            char_list[last_comma] = "|"
            last_comma = None
    return "".join(char_list)


def horn_to_prolog(clause):
    vars_or_lists = []
    clause = replace_spec_symbols(clause)
    parenthesis = regex.findall("\(.*?\)", clause)
    for par in parenthesis:
        vars_or_lists.extend(regex.split("\(|\)|,", par))
    vars_or_lists = [var for var in vars_or_lists if len(var) > 0]
    for var in vars_or_lists:
        if "nil" in var or "." in var:
            clause = clause.replace(var, list_translate(var))
    return clause


def replace_spec_symbols(clause, type="HLP"):
    if type == "HLP":
        clause = (
            clause.replace("<-", ":-")
            .replace(";", ".")
            .replace("?", "?-")
            .replace("\n", "")
            + "."
        )
    return clause


def translate(submission_id, type="HLP"):
    if type == "HLP":
        filename = SUBMISSIONS_DIRECTORY / (submission_id + ".pl")
        with open(filename, "r+") as horn_file:
            lines = horn_file.readlines()
        with open(filename, "w+") as horn_file:
            for clause in lines:
                print(horn_to_prolog(clause), file=horn_file)
