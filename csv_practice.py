# ISM2411 Lab 12 - Reflection
# 1. Python can process huge files, repeat the same steps, and be tracked in a version control, which is difficult to do with manual Excel clicks. Excel is better for quick, visual, and one-off exploration if you want to see and tweak the numbers by hand.
#
# 2. A store's point-of-sale system can append one line per transaction to a log. Append mode will add new lines without erasing previous ones, so the whole history is there for audits.

import csv
from datetime import datetime

SALES_FILE = "data/sales.csv"
CLEANED_FILE = "data/cleaned.csv"
LOG_FILE = "data/run_log.txt"

 # EXERCISE 1:
print("=== Exercise 1: Check the file ===")
with open(SALES_FILE, newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    data_rows = list(reader)
print("Header:", header)
print("Data rows:", len(data_rows))
assert header == ["product", "price", "quantity"], "Unexpected header"
assert len(data_rows) == 12, "Expected 12 data rows"

# EXERCISE 2:
print("\n=== Exercise 2: Raw rows ===")
with open(SALES_FILE, newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # every value is a string

# EXERCISE 3: 
print("\n=== Exercise 3: Skip the header ===")
with open(SALES_FILE, newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)

# EXERCISE 4: 
print("\n=== Exercise 4: Totals ===")
total_revenue = 0.0
with open(SALES_FILE, newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${total_revenue:.2f}")

# EXERCISE 5: 
print("\n=== Exercise 5: Filter and write ===")
original_count = 0
written_count = 0
with open(SALES_FILE, newline="") as infile, \
        open(CLEANED_FILE, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in reader:
        original_count += 1
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        total = price * quantity
        if total > 100:
            writer.writerow([product, f"{price:.2f}", quantity, f"{total:.2f}"])
            written_count += 1
print(f"Wrote {written_count} rows out of {original_count} in the original")

# EXERCISE 6: 
# Comparison: csv.reader is simple and fast but you must remember
# column positions (row[1]); DictReader uses names (row["price"]),
# which is clearer and survives column reordering, at slightly more overhead.
print("\n=== Exercise 6: DictReader ===")
dict_total = 0.0
with open(SALES_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        dict_total += line_total
        print(f"{row['product']}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue (DictReader): ${dict_total:.2f}")
print("Matches Exercise 4:", round(dict_total, 2) == round(total_revenue, 2))

# EXERCISE 7: 
print("\n=== Exercise 7: Summary by product ===")
summary = {}
with open(SALES_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        revenue = float(row["price"]) * int(row["quantity"])
        summary[row["product"]] = summary.get(row["product"], 0) + revenue
for product in sorted(summary):
    print(f"{product}: ${summary[product]:.2f}")

# EXERCISE 8: 
print("\n=== Exercise 8: Run log ===")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as log:
    log.write(f"{timestamp} - total revenue: ${total_revenue:.2f}\n")
print(f"Appended a line to {LOG_FILE}")