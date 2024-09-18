from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

import xlrd  # type: ignore

from mbl_xls_to_csv.utils import convert_date


@dataclass
class Statement:
    date: str
    description: str
    debit: Decimal
    credit: Decimal
    balance: Decimal


def parse_statement_from_xls(file_path: Path):
    rows: list[Statement] = []
    book: Any = xlrd.open_workbook(file_path)  # type: ignore
    sh = book.sheet_by_index(0)
    # mbl statement starts from row 14
    for rx in range(13, sh.nrows):
        date = sh.cell_value(rowx=rx, colx=3)
        ref = sh.cell_value(rowx=rx, colx=12)
        detail = sh.cell_value(rowx=rx, colx=18)
        debit = sh.cell_value(rowx=rx, colx=22)
        credit = sh.cell_value(rowx=rx, colx=23)
        balance = sh.cell_value(rowx=rx, colx=25)
        date = convert_date(date)
        if date and ref and detail:
            row = Statement(
                date=date,
                description=ref + ", " + detail,
                debit=Decimal(f"{debit:.2f}"),
                credit=Decimal(f"{credit:.2f}"),
                balance=Decimal(f"{balance:.2f}"),
            )
            rows.append(row)
    return rows
