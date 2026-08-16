"""Generate an Excel management report from finance transactions."""
from pathlib import Path
import pandas as pd


def build_report(input_file: str = "data/sample_transactions.csv", output_file: str = "outputs/finance_management_report.xlsx") -> Path:
    df = pd.read_csv(input_file)
    df["date"] = pd.to_datetime(df["date"])
    df["variance"] = df["amount"] - df["budget"]
    df["variance_pct"] = df["variance"] / df["budget"] * 100
    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly = df.groupby("month", as_index=False).agg(Budget=("budget", "sum"), Actual=("amount", "sum"))
    monthly["Variance"] = monthly["Actual"] - monthly["Budget"]
    monthly["Variance %"] = monthly["Variance"] / monthly["Budget"] * 100

    category = df.groupby("category", as_index=False).agg(Budget=("budget", "sum"), Actual=("amount", "sum"))
    category["Variance"] = category["Actual"] - category["Budget"]
    category["Variance %"] = category["Variance"] / category["Budget"] * 100
    category = category.sort_values("Actual", ascending=False)

    vendor = df.groupby("vendor", as_index=False).agg(Transactions=("transaction_id", "count"), Spend=("amount", "sum"))
    vendor = vendor.sort_values("Spend", ascending=False)

    duplicate = df[df.duplicated("invoice_no", keep=False)].sort_values("invoice_no")
    overruns = df[df["variance_pct"] > 10].sort_values("variance_pct", ascending=False)
    high_value = df[df["amount"] >= 150000].sort_values("amount", ascending=False)

    summary = pd.DataFrame({
        "Metric": ["Total Budget", "Total Actual", "Total Variance", "Variance %", "Transactions", "Duplicate Invoice Rows", "Budget Overruns >10%", "High Value Transactions"],
        "Value": [df["budget"].sum(), df["amount"].sum(), df["variance"].sum(), df["variance"].sum() / df["budget"].sum() * 100, len(df), len(duplicate), len(overruns), len(high_value)]
    })

    out = Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        summary.to_excel(writer, index=False, sheet_name="Executive Summary")
        monthly.to_excel(writer, index=False, sheet_name="Monthly Analysis")
        category.to_excel(writer, index=False, sheet_name="Category Analysis")
        vendor.to_excel(writer, index=False, sheet_name="Vendor Analysis")
        duplicate.to_excel(writer, index=False, sheet_name="Duplicate Invoices")
        overruns.to_excel(writer, index=False, sheet_name="Budget Exceptions")
        high_value.to_excel(writer, index=False, sheet_name="High Value")
        df.to_excel(writer, index=False, sheet_name="Transactions")

    return out


if __name__ == "__main__":
    print(f"Created: {build_report()}")
