"""Finance and accounting analysis functions."""
import pandas as pd


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["date"] = pd.to_datetime(work["date"])
    work["month"] = work["date"].dt.to_period("M").astype(str)
    return (
        work.groupby("month", as_index=False)
        .agg(budget=("budget", "sum"), actual=("amount", "sum"))
        .assign(variance=lambda x: x["actual"] - x["budget"])
        .assign(variance_pct=lambda x: x["variance"] / x["budget"] * 100)
    )


def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category", as_index=False)
        .agg(budget=("budget", "sum"), actual=("amount", "sum"))
        .assign(variance=lambda x: x["actual"] - x["budget"])
        .sort_values("actual", ascending=False)
    )


def vendor_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("vendor", as_index=False)
        .agg(transactions=("transaction_id", "count"), spend=("amount", "sum"))
        .sort_values("spend", ascending=False)
    )
