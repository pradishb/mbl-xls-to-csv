import csv
import json
import re

from PyPDF2 import PdfReader

date_re = "(\d{2})-(\d{2})-(\d{4})"
number_re = "[\d,]+\.\d+|-"


def get_date(parts):
    while parts:
        p = parts.pop(0)
        match = re.fullmatch(date_re, p)
        if match:
            # convert to m-d-y
            return match.group(2) + "-" + match.group(1) + "-" + match.group(3)
    return ""


def get_description(parts):
    desc = []
    while parts:
        p = parts.pop(0)
        date = re.fullmatch(date_re, p)
        number = re.fullmatch(number_re, p)
        if date is None and number is None:
            desc.append(p)
        else:
            parts.insert(0, p)
            return "".join(desc).replace(" ", "")
    return ""


def get_number(parts):
    while parts:
        p = parts.pop(0)
        if re.fullmatch(number_re, p):
            return float(p.replace(",", "").replace("-", "0"))
    return ""


def get_parts():
    parts = []

    def func(text, *args):
        if text:
            parts.append(text.strip())

    reader = PdfReader("input.pdf")
    for page in reader.pages:
        page.extract_text(visitor_text=func)
    return parts


def parse_statement():
    parts = get_parts()
    rows = []
    while parts:
        row = {
            "date": get_date(parts),
            "description": get_description(parts),
            "debit": get_number(parts),
            "credit": get_number(parts),
            "balance": get_number(parts),
        }
        if row["date"]:
            rows.append(row)
    return rows


if __name__ == "__main__":
    statement = parse_statement()
    with open("transaction_reference.json") as fp:
        ref = json.load(fp)
    with open("output.csv", "w", newline="") as fp:
        writer = csv.writer(fp, delimiter=";")
        for s in statement:
            if s["debit"] > 0 and s["credit"] > 0:
                print("bad row, debit and credit both greater than 0", r)
                continue
            if s["credit"] > 0:
                print("credit is not supported", s)
                continue
            for r in ref:
                if r["substring"] in s["description"]:
                    writer.writerow(
                        [
                            s["date"],
                            4,
                            "",
                            "",
                            ",".join([r["memo"], s["description"]]),
                            s["debit"] * -1,
                            r["category"],
                            "",
                        ]
                    )
                    break
            else:
                print(r["description"], "not found in reference")
