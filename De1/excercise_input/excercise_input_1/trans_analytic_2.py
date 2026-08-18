import argparse
import csv
from collections import Counter
from pathlib import Path

def analyze_2(input_file, output_file):

  user_products = Counter()
  product_buyer = {}

  with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      if not row["user"] or row["user"].strip == "" or row["user"].lower() == "null":
        continue
      
      if int(row["status"]) == 1:
        product = row["product"]
        user = row["user"]

        if product not in product_buyer:
            product_buyer[product] = set()

        product_buyer[product].add(user)      
  product_count = {
      product: len(buyers)
      for product, buyers in product_buyer.items()
  }

  top_10 = sorted(
     product_count.items(),
     key=lambda x: x[1],
     reverse=True
  )[:10]

  output_1 = Path(output_file)

  output_1.parent.mkdir(parents=True,exist_ok=True)

  with open(output_1,"w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
          "Most_buyer_products",
          "Count"
        ]
    )
    for product, count in top_10:
        writer.writerow(
          [
            product,
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

        analyze_2(
            args.input,
            args.output
        )

if __name__ == "__main__":

    main()
