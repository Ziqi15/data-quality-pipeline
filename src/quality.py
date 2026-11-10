"""Data-quality rules for cleaned transactions.

Each rule returns the rows that break it. The script exits with code 1 if any
rule fails, so a GitHub Actions run turns red when the data is not trustworthy.

Usage:
    python src/quality.py output/clean_transactions.csv
"""

import sys

import pandas as pd

from clean import VALID_CATEGORIES


def missing_customer_id(df):
    return df[df["customer_id"].isna()]


def invalid_date(df):
    return df[df["date"].isna()]


def non_positive_amount(df):
    return df[df["amount"].isna() | (df["amount"] <= 0)]


def unknown_category(df):
    return df[~df["category"].isin(VALID_CATEGORIES)]


def duplicate_transaction_id(df):
    return df[df["transaction_id"].duplicated(keep=False)]


RULES = {
    "missing customer_id": missing_customer_id,
    "invalid date": invalid_date,
    "missing or non-positive amount": non_positive_amount,
    "unknown category": unknown_category,
    "duplicate transaction_id": duplicate_transaction_id,
}


def run_checks(df):
    """Return {rule name: list of failing transaction_ids} for every rule that fails."""
    failures = {}
    for name, rule in RULES.items():
        bad = rule(df)
        if not bad.empty:
            failures[name] = bad["transaction_id"].tolist()
    return failures


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    df = pd.read_csv(argv[1], parse_dates=["date"], dtype={"customer_id": "string"})
    failures = run_checks(df)
    if not failures:
        print(f"All {len(RULES)} data-quality rules passed on {len(df)} rows.")
        return 0
    print(f"{len(failures)} of {len(RULES)} data-quality rules failed:")
    for name, ids in failures.items():
        print(f"  - {name}: {', '.join(ids)}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
