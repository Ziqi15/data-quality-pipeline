import pandas as pd

from quality import run_checks


def cleaned(rows):
    df = pd.DataFrame(rows, columns=["transaction_id", "customer_id", "date", "category", "amount"])
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


GOOD = ["T1", "C1", "2026-09-01", "Dining", 10.0]


def test_clean_data_passes_every_rule():
    assert run_checks(cleaned([GOOD])) == {}


def test_missing_customer_is_flagged():
    failures = run_checks(cleaned([["T1", None, "2026-09-01", "Dining", 10.0]]))
    assert failures == {"missing customer_id": ["T1"]}


def test_negative_amount_is_flagged():
    failures = run_checks(cleaned([["T1", "C1", "2026-09-01", "Dining", -5.0]]))
    assert "missing or non-positive amount" in failures


def test_unknown_category_is_flagged():
    failures = run_checks(cleaned([["T1", "C1", "2026-09-01", "Gambling", 10.0]]))
    assert failures == {"unknown category": ["T1"]}


def test_duplicate_id_is_flagged():
    failures = run_checks(cleaned([GOOD, ["T1", "C2", "2026-09-02", "Dining", 20.0]]))
    assert failures == {"duplicate transaction_id": ["T1", "T1"]}
