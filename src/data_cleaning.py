"""Basic data quality checks for finance transactions."""
import pandas as pd

REQUIRED_COLUMNS = {
    "transaction_id", "date", "invoice_no", "vendor", "category",
    "department", "budget", "amount"
}


def validate_schema(df: pd.DataFrame) -> list[str]:
    return sorted(REQUIRED_COLUMNS - set(df.columns))


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["date"] = pd.to_datetime(work["date"], errors="coerce")
    work["budget"] = pd.to_numeric(work["budget"], errors="coerce")
    work["amount"] = pd.to_numeric(work["amount"], errors="coerce")
    work["vendor"] = work["vendor"].str.strip()
    work["category"] = work["category"].str.strip()
    return work
