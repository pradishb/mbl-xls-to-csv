import re
from decimal import Decimal

from PyPDF2 import PdfReader

from utils import convert_date
from utils import date_re

number_re = "[\d,]+\.\d+|-"


def get_date(parts):
    while parts:
        p = parts.pop(0)
        date = convert_date(p)
        if date:
            return date
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
            return Decimal(p.replace(",", "").replace("-", "0"))
    return ""


def get_parts(file_path):
    parts = []

    def func(text, *args):
        if text:
            parts.append(text.strip())

    reader = PdfReader(file_path)
    for page in reader.pages:
        page.extract_text(visitor_text=func)
    return parts


def parse_statement_from_pdf(file_path):
    parts = get_parts(file_path)
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
