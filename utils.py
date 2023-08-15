import re

date_re = "(\d{2})-(\d{2})-(\d{4})"


def convert_date(string):
    match = re.fullmatch(date_re, string)
    if match:
        # convert to m-d-y
        return match.group(2) + "-" + match.group(1) + "-" + match.group(3)
    match = re.fullmatch("(\d{4})-(\d{2})-(\d{2})", string)
    if match:
        # convert to m-d-y
        return match.group(2) + "-" + match.group(3) + "-" + match.group(1)
    return ""
