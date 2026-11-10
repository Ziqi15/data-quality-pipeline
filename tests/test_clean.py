import pandas as pd

from clean import clean, summarise


def raw(rows):
    return pd.DataFrame(rows, columns=["transaction_id", "customer_id", "date", "category", "amount"], dtype=str)


def test_trims_and_standardises_category():
    df = clean(raw([["T1", "C1", "2026-09-01", " groceries ", "10"]]))
    assert df.loc[0, "category"] == "Groceries"


def test_bad_date_becomes_missing():
    df = clean(raw([["T1", "C1", "not a date", "Dining", "10"]]))
    assert pd.isna(df.loc[0, "date"])


def test_amount_is_numeric():
    df = clean(raw([["T1", "C1", "2026-09-01", "Dining", "12.50"]]))
    assert df.loc[0, "amount"] == 12.50


def test_exact_duplicates_are_dropped():
    row = ["T1", "C1", "2026-09-01", "Dining", "10"]
    assert len(clean(raw([row, row]))) == 1


def test_summary_sorted_by_total():
    df = clean(raw([
        ["T1", "C1", "2026-09-01", "Dining", "10"],
        ["T2", "C2", "2026-09-01", "Groceries", "50"],
        ["T3", "C3", "2026-09-02", "Groceries", "5"],
    ]))
    summary = summarise(df)
    assert summary.loc[0, "category"] == "Groceries"
    assert summary.loc[0, "transactions"] == 2
