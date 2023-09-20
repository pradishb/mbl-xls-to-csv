import csv
import json
from argparse import ArgumentParser
from decimal import Decimal
from pathlib import Path

from pdf import parse_statement_from_pdf
from xls import parse_statement_from_xls


def get_is_substr(sub: str, text: str):
    return sub.replace(" ", "").upper() in text.replace(" ", "").upper()


def main():
    parser = ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--start")
    args = parser.parse_args()
    file_path = Path(args.input)

    if file_path.suffix not in [".xls", ".pdf"]:
        print("Invalid input format")
        return

    current_balance = args.start
    if file_path.suffix == ".pdf":
        statement = parse_statement_from_pdf(file_path)
    else:
        statement = parse_statement_from_xls(file_path)
    if current_balance:
        try:
            balance_list = [s["balance"] for s in statement]
            idx = balance_list.index(Decimal(current_balance))
            statement = statement[idx + 1 :]
        except ValueError:
            print(f"Balance {current_balance} missing in the statement.")
            return
    try:
        with open("transaction_reference.json") as fp:
            ref = json.load(fp)
    except FileNotFoundError:
        ref = []
    with open("output.csv", "w", newline="") as fp:
        writer = csv.writer(fp, delimiter=";")
        for s in statement:
            if s["debit"] > 0 and s["credit"] > 0:
                print("bad row, debit and credit both greater than 0", r)
                continue
            elif s["credit"] > 0:
                for r in ref:
                    if get_is_substr(r["substring"], s["description"]):
                        writer.writerow(
                            [
                                s["date"],
                                4,
                                "",
                                "",
                                "".join([r["memo"], s["description"]]),
                                s["credit"],
                                r["category"],
                                "",
                            ]
                        )
                        break
                else:
                    print("Not found in reference", s)
                    writer.writerow(
                        [
                            s["date"],
                            4,
                            "",
                            "",
                            s["description"],
                            s["credit"],
                            "",
                            "",
                        ]
                    )
            elif s["debit"] > 0:
                for r in ref:
                    if get_is_substr(r["substring"], s["description"]):
                        writer.writerow(
                            [
                                s["date"],
                                4,
                                "",
                                "",
                                ", ".join([r["memo"], s["description"]]),
                                s["debit"] * -1,
                                r["category"],
                                "",
                            ]
                        )
                        break
                else:
                    print("Not found in reference", s)
                    writer.writerow(
                        [
                            s["date"],
                            4,
                            "",
                            "",
                            s["description"],
                            s["debit"] * -1,
                            "",
                            "",
                        ]
                    )


if __name__ == "__main__":
    main()
