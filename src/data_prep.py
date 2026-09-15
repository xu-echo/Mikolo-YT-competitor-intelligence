import pandas as pd
import numpy as np
from .config import MAJOR_FILE, RITFIT_FILE, PROCESSED_DIR

COLUMNS = [
    "Date", "Content", "Content link", "Influencer", "Type", "Tags",
    "Estimated cost", "CPM", "Subscribers", "Region", "Promotion type",
    "Engagement rate", "Views", "Likes", "Comments"
]

def load_sources():
    # The uploaded Excel contains a pivot sheet and the actual content sheet.
    major = pd.read_excel(MAJOR_FILE, sheet_name="noxinfluencer_brand_monitor_con")
    ritfit = pd.read_csv(RITFIT_FILE)
    major["Brand"] = "Major Fitness"
    ritfit["Brand"] = "RITFIT"
    return major, ritfit

def standardize(df):
    df = df.copy()
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["Date"] = pd.to_datetime(df["Date"], format="mixed", errors="coerce")
    for c in ["Estimated cost", "CPM", "Subscribers", "Engagement rate", "Views", "Likes", "Comments"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    text_cols = ["Content", "Content link", "Influencer", "Type", "Tags", "Region", "Promotion type"]
    for c in text_cols:
        df[c] = df[c].fillna("").astype(str).str.strip()

    # Derived metrics
    df["Like rate"] = np.where(df["Views"] > 0, df["Likes"] / df["Views"], np.nan)
    df["Comment rate"] = np.where(df["Views"] > 0, df["Comments"] / df["Views"], np.nan)
    df["Calculated ER"] = np.where(
        df["Views"] > 0, (df["Likes"] + df["Comments"]) / df["Views"], np.nan
    )
    df["Views per 1K subscribers"] = np.where(
        df["Subscribers"] > 0, df["Views"] / df["Subscribers"] * 1000, np.nan
    )
    df["Cost per 1K views"] = np.where(
        df["Views"] > 0, df["Estimated cost"] / df["Views"] * 1000, np.nan
    )
    df["Views per dollar"] = np.where(
        df["Estimated cost"] > 0, df["Views"] / df["Estimated cost"], np.nan
    )

    # Creator tier based on subscriber count at the time of the observed video.
    bins = [-1, 10_000, 50_000, 100_000, 500_000, float("inf")]
    labels = ["Nano", "Micro", "Mid", "Macro", "Mega"]
    df["Creator tier"] = pd.cut(df["Subscribers"], bins=bins, labels=labels)

    # Month for trend analysis
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    # Simple content taxonomy based on source fields.
    text = (df["Type"] + " " + df["Tags"] + " " + df["Content"]).str.lower()
    rules = [
        ("Home Gym / Garage Gym", r"home gym|garage gym|homegym|garagegym"),
        ("Equipment Review", r"review|reviews|testing|test|equipment"),
        ("Strength / Training", r"workout|fitness|strength|bodybuilding|kettlebell|training|powerlifting"),
        ("Running / Endurance", r"running|run |marathon|triathlon|endurance|cardio|cycling"),
        ("Lifestyle / Vlog", r"vlog|lifestyle|life style|day in"),
        ("DIY / Build", r"\bdiy\b|build|building|setup|set up|con "),
        ("Sports / Athlete", r"sports|athlete|olympic|baseball|football|basketball"),
        ("Health / Nutrition", r"health|nutrition|food|diet"),
        ("Tech / Gadget", r"technology|tech|gadget|consumer electronic"),
    ]
    df["Content theme"] = "Other"
    for theme, pattern in rules:
        mask = text.str.contains(pattern, regex=True, na=False)
        df.loc[mask & (df["Content theme"] == "Other"), "Content theme"] = theme

    return df

def main():
    major, ritfit = load_sources()
    df = pd.concat([standardize(major), standardize(ritfit)], ignore_index=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out = PROCESSED_DIR / "combined_youtube_content.csv"
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} rows -> {out}")
    print(df.groupby("Brand").size())
    return df

if __name__ == "__main__":
    main()
