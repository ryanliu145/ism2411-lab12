import csv

INPUT_FILE = "data/sales.csv"
OUTPUT_FILE = "data/cleaned_report.csv"


def read_sales(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def clean_rows(rows):
    cleaned = []
    for row in rows:
        row = {k.strip(): (v or "").strip() for k, v in row.items()}
        if not all(row.values()):
            continue
        try:
            row["quantity"] = int(row["quantity"])
            row["price"] = float(row["price"])
        except (KeyError, ValueError):
            continue
        row["total"] = round(row["quantity"] * row["price"], 2)
        cleaned.append(row)
    return cleaned


def write_report(rows, path):
    if not rows:
        print("No valid rows to write.")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = read_sales(INPUT_FILE)
    cleaned = clean_rows(rows)
    write_report(cleaned, OUTPUT_FILE)
    print(f"Read {len(rows)} rows, wrote {len(cleaned)} cleaned rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()