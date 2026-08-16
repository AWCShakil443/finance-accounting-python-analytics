"""Create finance analytics dashboard charts from the synthetic transaction data."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

INPUT = Path("data/sample_transactions.csv")
OUTPUT = Path("outputs/charts")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT, parse_dates=["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["variance"] = df["amount"] - df["budget"]
    df["variance_pct"] = df["variance"] / df["budget"] * 100

    monthly = df.groupby("month", as_index=False).agg(Budget=("budget", "sum"), Actual=("amount", "sum"))
    monthly["Variance"] = monthly["Actual"] - monthly["Budget"]
    monthly.plot(x="month", y=["Budget", "Actual"], kind="bar", figsize=(9, 5), title="Monthly Budget vs Actual")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(OUTPUT / "01_budget_vs_actual.png", dpi=160)
    plt.close()

    category = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    category.plot(kind="bar", figsize=(9, 5), title="Spend by Category")
    plt.ylabel("Actual Spend")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT / "02_spend_by_category.png", dpi=160)
    plt.close()

    vendor = df.groupby("vendor")["amount"].sum().sort_values(ascending=True)
    vendor.plot(kind="barh", figsize=(9, 5), title="Vendor Spend Concentration")
    plt.xlabel("Spend")
    plt.tight_layout()
    plt.savefig(OUTPUT / "03_vendor_concentration.png", dpi=160)
    plt.close()

    exceptions = pd.Series({
        "Duplicate invoices": int(df.duplicated("invoice_no", keep=False).sum()),
        "Budget overruns >10%": int((df["variance_pct"] > 10).sum()),
        "High value >=150k": int((df["amount"] >= 150000).sum()),
    })
    exceptions.plot(kind="bar", figsize=(8, 5), title="Exception Testing Summary")
    plt.ylabel("Number of Rows")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT / "04_exception_summary.png", dpi=160)
    plt.close()

    print(f"Dashboard charts created in {OUTPUT.resolve()}")


if __name__ == "__main__":
    main()
