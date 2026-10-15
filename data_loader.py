"""Load the bundled synthetic CSV and compute Hour 1 summaries (no database)."""
from pathlib import Path

import pandas as pd

SAMPLE_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_consumption.csv"
REQUIRED_COLUMNS = ["date", "building", "resource", "consumption", "unit", "unit_cost"]
RESOURCE_ORDER = ["electricity", "water", "paper"]


def load_sample() -> pd.DataFrame:
    df = pd.read_csv(SAMPLE_PATH)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Sample CSV is missing columns: {missing}")
    df["date"] = pd.to_datetime(df["date"])
    df["cost"] = df["consumption"] * df["unit_cost"]  # INR = consumption x unit_cost
    return df


def build_payload(df: pd.DataFrame, limit: int = 50) -> dict:
    """Summary + preview rows. Resources are aggregated separately (units never mixed)."""
    if df.empty:
        return {"synthetic": True, "currency": "INR", "meta": None, "summary": [], "records": []}

    summary = []
    for resource in RESOURCE_ORDER:
        sub = df[df["resource"] == resource]
        if sub.empty:
            continue
        summary.append(
            {
                "resource": resource,
                "unit": str(sub["unit"].iloc[0]),
                "total_consumption": round(float(sub["consumption"].sum()), 2),
                "total_cost": round(float(sub["cost"].sum()), 2),
                "records": int(len(sub)),
            }
        )

    preview = df.head(limit).copy()
    preview["date"] = preview["date"].dt.strftime("%Y-%m-%d")
    preview["cost"] = preview["cost"].round(2)

    return {
        "synthetic": True,
        "currency": "INR",
        "meta": {
            "total_records": int(len(df)),
            "buildings": int(df["building"].nunique()),
            "date_start": df["date"].min().strftime("%Y-%m-%d"),
            "date_end": df["date"].max().strftime("%Y-%m-%d"),
            "preview_rows": int(len(preview)),
        },
        "summary": summary,
        "records": preview[REQUIRED_COLUMNS + ["cost"]].to_dict(orient="records"),
    }
