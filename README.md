# Data Quality Pipeline

A small Python pipeline that cleans a raw transactions file and checks it against data-quality rules before it is used for analysis. GitHub Actions runs the tests and the checks on every push and pull request, so untrustworthy data turns the build red.

Built for my 43030 Professional Learning Plan (Goal 3: software development tools).

## What it does

1. `src/clean.py` trims spaces, standardises category names, converts dates and amounts, removes exact duplicates, and prints spend by category.
2. `src/quality.py` checks five rules: missing customer ID, invalid date, missing or non-positive amount, unknown category, duplicate transaction ID. It exits with code 1 and lists the failing rows if any rule fails.
3. `.github/workflows/ci.yml` runs the unit tests, the cleaning step and the quality checks, then uploads the cleaned file as a build artifact.

## Run it locally

```bash
pip install -r requirements.txt
pytest -v
python src/clean.py data/sample_transactions.csv output/clean_transactions.csv
python src/quality.py output/clean_transactions.csv
```

## Data

`data/sample_transactions.csv` is synthetic sample data. It contains deliberate errors so the quality checks have something to catch.
