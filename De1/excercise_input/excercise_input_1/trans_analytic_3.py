import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime

def analyze_3(input_file, output_file):

    user_transactions = Counter()
    all_rows = []

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            all_rows.append(row)
            user_transactions[row["user"]] += 1 


    top_10_users = [user for user, _ in user_transactions.most_common(10)]

    user_day_rows = defaultdict(lambda: defaultdict(list))

    for row in all_rows:
      if row["user"] in top_10_users:


        timestamp_seconds = int(row["timestamp"]) / 1000 
        
        ts = datetime.fromtimestamp(timestamp_seconds)

        day = ts.date() # Lấy ra ngày tháng năm (YYYY-MM-DD)

        user_day_rows[row["user"]][day].append((ts, row["product"]))

    result = []

    for user in top_10_users:
        for day, transactions in user_day_rows[user].items():
            first_product = sorted(transactions, key=lambda x: x[0])[0][1]
            result.append((user, str(day), first_product))


    output_3 = Path(output_file)

    output_3.parent.mkdir(parents=True,exist_ok=True)

    with open(output_3,"w", encoding="utf-8", newline="") as f:
      writer = csv.writer(f)
      writer.writerow(
        [
          "user",
          "date",
          "first_products_of_day"
        ]
      )
      for row in result:
        writer.writerow(row)
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

        analyze_3(
            args.input,
            args.output
        )

if __name__ == "__main__":

    main()
