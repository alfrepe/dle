import re

expr1 = "^(Conjug. |Del |De |Quizá ).+"
expr2 = "^\d+\.\s\w+\.\s(\w+\.\s)?"

def ignore_by_regex(lines):
    lines_output = []
    # https://docs.python.org/3/library/re.html#re.compile
    pattern = re.compile(expr1, re.IGNORECASE)
    for line in lines:
        if pattern.match(line):
            continue
        lines_output.append(re.sub(expr2, "", line))
    return lines_output
