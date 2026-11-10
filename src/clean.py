"""Clean a raw transactions CSV so it is ready for analysis.

Usage:
    python src/clean.py data/sample_transactions.csv output/clean_transactions.csv
"""

import sys
from pathlib import Path

import pandas as pd

VALID_CATEGORIES = {"Groceries", "Transport", "Dining", "Utilities", "Entertainment"}


def load(path):
    """Read the raw CSV, keeping every column as text so nothing is silently converted."""
    return pd.read_csv(path, dtype=str)


def clean(df):
    """Return a cleaned copy of the raw transactions.

    Steps:
    1. Trim spaces from every text value.
    2. Standardise category names to Title Case ("groceries " -> "Groceries").
    3. Convert dates and amounts to proper types; bad values become missing (NaT / NaN).
    4. Drop exact duplicate rows.
    """
    out = df.copy()
    for col in out.columns:
        out[col] = out[col].str.strip()

    out["category"] = out["category"].str.title()
    out["date"] = pd.to_datetime(out["date"], format="%Y-%m-%d", errors="coerce")
    out["amount"] = pd.to_numeric(out["amount"], errors="coerce")
    out["customer_id"] = out["customer_id"].replace("", pd.NA)

    out = out.drop_duplicates().reset_index(drop=True)
    return out


def summarise(df):
    """Total spend and number of transactions per category, largest first."""
    return (
        df.groupby("category", as_index=False)
        .agg(transactions=("transaction_id", "count"), total_amount=("amount", "sum"))
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    raw_path, out_path = argv[1], Path(argv[2])
    cleaned = clean(load(raw_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(out_path, index=False)
    print(f"Cleaned {len(cleaned)} rows -> {out_path}")
    print(summarise(cleaned).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
