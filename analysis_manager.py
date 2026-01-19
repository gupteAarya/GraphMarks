import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import os
import df_manager

def generate_line_graph(months=None, test_type=None):

    test_name = {
    "PAT": "📘 Part Test",
    "ADV": "⏱️ 6 Hour Advanced",
    "JEM": "🎯 JEE Main"
    }.get(test_type, "📝 Test")
    
    df = df_manager.get_marks_df(test_type=test_type)

    if df.empty:
        return None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    if months is not None:
        cutoff = pd.Timestamp.today() - pd.DateOffset(months=months)
        df = df[df["date"] >= cutoff]

    if len(df) < 1:
        return None

    os.makedirs("static", exist_ok=True)
    path = f"static/marks_{test_type}.png"

    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax2 = ax1.twinx()

    ax1.plot(df["date"], df["physics"], marker="o", label="Physics")
    ax1.plot(df["date"], df["chemistry"], marker="o", label="Chemistry")
    ax1.plot(df["date"], df["maths"], marker="o", label="Maths")

    ax2.plot(df["date"], df["total"], marker="o", linestyle="--", label="Total")

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Subject Marks")
    ax2.set_ylabel("Total Marks")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2)

    plt.title(f"{test_name} Progress Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return path


def calculate_improvement(months, test_type):
    df = df_manager.get_marks_df(test_type=test_type)

    if df.empty:
        return {}

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    last_date = df["date"].max()
    cutoff = last_date - pd.DateOffset(months=months)
    df = df[df["date"] >= cutoff]

    improvements = {}
    cols = ["physics", "chemistry", "maths", "total"]

    for col in cols:
        if len(df[col]) < 2:
            improvements[col] = None
            continue

        first = df[col].iloc[0]
        last = df[col].iloc[-1]

        if first == 0:
            improvements[col] = None
        else:
            improvements[col] = round(((last - first) / first) * 100, 2)

    return improvements

def calculate_latest_and_total_improvement(test_type):
    df = df_manager.get_marks_df(test_type)

    if df.empty or len(df) < 2:
        return {}, {}  # Not enough data to calculate

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    cols = ["physics", "chemistry", "maths", "total"]

    latest_improvement = {}
    total_improvement = {}

    for col in cols:
        # Latest improvement: last entry vs previous entry
        prev = df[col].iloc[-2]
        curr = df[col].iloc[-1]
        latest_improvement[col] = round(((curr - prev) / prev) * 100, 2) if prev != 0 else None

        # Total improvement: last entry vs first entry
        first = df[col].iloc[0]
        total_improvement[col] = round(((curr - first) / first) * 100, 2) if first != 0 else None

    return latest_improvement, total_improvement
