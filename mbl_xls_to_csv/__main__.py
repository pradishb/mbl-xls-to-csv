import csv
from argparse import ArgumentParser
from decimal import Decimal
from pathlib import Path

from mbl_xls_to_csv.xls import parse_statement_from_xls


def get_is_substr(sub: str, text: str):
    return sub.replace(" ", "").upper() in text.replace(" ", "").upper()


def main():
    parser = ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--start")
    parser.add_argument("--delimiter", default=";")
    args = parser.parse_args()
    file_path = Path(args.input)

    if file_path.suffix not in [".xls", ".pdf"]:
        print("Invalid input format")
        return

    current_balance = args.start
    statement = parse_statement_from_xls(file_path)
    if current_balance:
        try:
            current_balance = current_balance.replace(",", "")
            balance_list = [s.balance for s in statement]
            idx = balance_list.index(Decimal(current_balance))
            statement = statement[idx + 1 :]
        except ValueError:
            print(f"Balance {current_balance} missing in the statement.")
            return
    with open("output.csv", "w", newline="") as fp:
        writer = csv.writer(fp, delimiter=args.delimiter)
        for s in statement:
            if s.debit > 0 and s.credit > 0:
                print("bad row, debit and credit both greater than 0", s)
                continue
            elif s.credit > 0:
                writer.writerow(
                    [
                        s.date,
                        4,
                        "",
                        "",
                        s.description,
                        s.credit,
                        "",
                        "",
                    ]
                )
            elif s.debit > 0:
                writer.writerow(
                    [
                        s.date,
                        4,
                        "",
                        "",
                        s.description,
                        s.debit * -1,
                        "",
                        "",
                    ]
                )


if __name__ == "__main__":
    main()
