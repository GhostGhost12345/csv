import argparse
import csv

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="Path to CSV file")
    parser.add_argument("--where", help='Filter condition, e.g. "price>500"')
    parser.add_argument("--aggregate", help='Aggregate, e.g. "price=avg"')
    return parser.parse_args()

def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def cast_value(value):
    try:
        return float(value)
    except ValueError:
        return value

def apply_filter(rows, condition):
    valid_ops = (">", "<", "=")
    op_used = None
    for op in valid_ops:
        if condition.count(op) == 1:
            op_used = op
            break
    if not op_used:
        raise ValueError(f"Invalid filter condition: {condition}")

    column, value = condition.split(op_used, 1)
    column = column.strip()
    value = cast_value(value.strip())
    filtered = []
    for row in rows:
        cell = cast_value(row[column])
        if op_used == ">" and cell > value:
            filtered.append(row)
        elif op_used == "<" and cell < value:
            filtered.append(row)
        elif op_used == "=" and cell == value:
            filtered.append(row)
    return filtered

def avg(values):
    return sum(values) / len(values) if values else 0

def apply_aggregate(rows, condition):
    if "=" not in condition:
        raise ValueError("Invalid aggregate condition")
    column, func = map(str.strip, condition.split("=", 1))
    values = [float(row[column]) for row in rows]

    if func == "avg":
        result = avg(values)
    elif func == "min":
        result = min(values)
    elif func == "max":
        result = max(values)
    else:
        raise ValueError("Unsupported aggregation function")

    return {f"{func}({column})": result}

def print_table(data):
    if not data:
        print("No data to display.")
        return
    headers = list(data[0].keys())
    widths = {h: max(len(h), *(len(str(row[h])) for row in data)) for h in headers}
    print(" | ".join(h.ljust(widths[h]) for h in headers))
    print("-+-".join("-" * widths[h] for h in headers))
    for row in data:
        print(" | ".join(str(row[h]).ljust(widths[h]) for h in headers))

def main():
    args = parse_args()
    rows = load_csv(args.csv_path)

    if args.where and args.aggregate:
        print("Error: Specify only one of --where or --aggregate")
        return

    if args.where:
        try:
            filtered = apply_filter(rows, args.where)
            print_table(filtered)
        except Exception as e:
            print(f"Filter error: {e}")
    elif args.aggregate:
        try:
            agg = apply_aggregate(rows, args.aggregate)
            print_table([agg])
        except Exception as e:
            print(f"Aggregate error: {e}")
    else:
        print_table(rows)

if __name__ == "__main__":
    main()
