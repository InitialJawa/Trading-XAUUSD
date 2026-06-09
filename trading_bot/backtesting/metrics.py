import json
import os

import pandas as pd

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data"
)


def load_trade_history():
    archive_dir = os.path.join(DATA_DIR, "archive")
    if not os.path.exists(archive_dir):
        return pd.DataFrame()

    records = []
    for fname in sorted(os.listdir(archive_dir)):
        if fname.endswith(".json"):
            with open(os.path.join(archive_dir, fname)) as f:
                data = json.load(f)
                records.extend(data)

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.sort_values("timestamp", inplace=True)
    return df


def compute_performance():
    df = load_trade_history()
    if df.empty:
        return {"error": "No trade history found"}

    metrics = {
        "total_snapshots": len(df),
        "date_range": {
            "start": str(df["timestamp"].min()),
            "end": str(df["timestamp"].max()),
        },
        "signals_distribution": df["composite_signal"].apply(
            lambda x: x.get("decision") if isinstance(x, dict) else None
        ).value_counts().to_dict() if "composite_signal" in df.columns else {}
    }

    if "price" in df.columns:
        prices = df["price"].apply(lambda x: x.get("close") if isinstance(x, dict) else None)
        prices = prices.dropna()

        if len(prices) > 1:
            total_return = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
            metrics["price_tracking"] = {
                "first": prices.iloc[0],
                "last": prices.iloc[-1],
                "total_return_pct": round(total_return, 2),
                "high": prices.max(),
                "low": prices.min(),
            }

    return metrics


if __name__ == "__main__":
    import json
    print(json.dumps(compute_performance(), indent=4))
