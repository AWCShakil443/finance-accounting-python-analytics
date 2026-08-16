"""Exception tests useful for finance and internal audit analytics."""
import pandas as pd


def duplicate_invoice_test(df: pd.DataFrame) -> pd.DataFrame:
    counts = df.groupby("invoice_no")["transaction_id"].transform("count")
    return df[counts > 1].copy()


def budget_overrun_test(df: pd.DataFrame, threshold_pct: float = 10) -> pd.DataFrame:
    work = df.copy()
    work["variance_pct"] = (work["amount"] - work["budget"]) / work["budget"] * 100
    return work[work["variance_pct"] > threshold_pct].sort_values("variance_pct", ascending=False)


def high_value_test(df: pd.DataFrame, threshold: float = 150000) -> pd.DataFrame:
    return df[df["amount"] >= threshold].sort_values("amount", ascending=False).copy()
