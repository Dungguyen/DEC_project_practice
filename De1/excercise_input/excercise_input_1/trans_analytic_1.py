import argparse
import csv
from collections import Counter
from pathlib import Path

def analyze(input_file, output_file):

    user_transactions = Counter()

    with open(input_file, "r", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:
            if int(row["status"]) == 1:
                user = row["user"]
                user_transactions[user] += 1

        top_10 = user_transactions.most_common(10)

        output_1 = Path(output_file)

        output_1.parent.mkdir(parents=True,exist_ok=True)

        with open(output_1,"w",encoding="utf-8",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "user",
                    "successful_transactions"
                ]
            )
            for user, count in top_10:
                writer.writerow(
                    [
                        user,
                        count
                    ]
                )
def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    run = subparsers.add_parser(
        "run"
    )

    run.add_argument(
        "--input",
        required=True
    )

    run.add_argument(
        "--output",
        required=True
    )

    args = parser.parse_args()

    if args.command == "run":

        analyze(
            args.input,
            args.output
        )

if __name__ == "__main__":

    main()
