import pandas as pd
import numpy as np
from .config import PROCESSED_DIR

INPUT = PROCESSED_DIR / "combined_youtube_content.csv"

def load():
    return pd.read_csv(INPUT, parse_dates=["Date"])

def creator_summary(df):
    return (
        df.groupby(["Brand", "Influencer"], as_index=False)
        .agg(
            collaborations=("Content link", "nunique"),
            subscribers=("Subscribers", "max"),
            total_views=("Views", "sum"),
            avg_views=("Views", "mean"),
            median_views=("Views", "median"),
            avg_engagement=("Engagement rate", "mean"),
            avg_calculated_er=("Calculated ER", "mean"),
            total_likes=("Likes", "sum"),
            total_comments=("Comments", "sum"),
            estimated_cost=("Estimated cost", "sum"),
            avg_cost_per_1k_views=("Cost per 1K views", "mean"),
            avg_views_per_1k_subscribers=("Views per 1K subscribers", "mean"),
        )
        .sort_values(["Brand", "total_views"], ascending=[True, False])
    )

def competitor_summary(df):
    return (
        df.groupby("Brand", as_index=False)
        .agg(
            videos=("Content link", "nunique"),
            creators=("Influencer", "nunique"),
            total_views=("Views", "sum"),
            avg_views=("Views", "mean"),
            median_views=("Views", "median"),
            avg_engagement=("Engagement rate", "mean"),
            estimated_cost=("Estimated cost", "sum"),
            avg_cost_per_1k_views=("Cost per 1K views", "mean"),
            sponsored=("Promotion type", lambda x: (x == "Sponsored").sum()),
            mentioned=("Promotion type", lambda x: (x == "Mentioned").sum()),
            suspected=("Promotion type", lambda x: (x == "Suspected").sum()),
        )
    )

def creator_overlap(df):
    major = set(df.loc[df["Brand"] == "Major Fitness", "Influencer"])
    ritfit = set(df.loc[df["Brand"] == "RITFIT", "Influencer"])
    overlap = sorted(major & ritfit)
    rows = []
    for creator in overlap:
        sub = df[df["Influencer"] == creator]
        rows.append({
            "Influencer": creator,
            "Major collaborations": (sub["Brand"] == "Major Fitness").sum(),
            "RITFIT collaborations": (sub["Brand"] == "RITFIT").sum(),
            "Major views": sub.loc[sub["Brand"] == "Major Fitness", "Views"].sum(),
            "RITFIT views": sub.loc[sub["Brand"] == "RITFIT", "Views"].sum(),
            "Subscribers": sub["Subscribers"].max(),
        })
    return pd.DataFrame(rows).sort_values("Major views", ascending=False)

def collaboration_type_summary(df):
    return (
        df.groupby(["Brand", "Promotion type"], as_index=False)
        .agg(
            videos=("Content link", "nunique"),
            creators=("Influencer", "nunique"),
            total_views=("Views", "sum"),
            avg_views=("Views", "mean"),
            avg_engagement=("Engagement rate", "mean"),
            avg_cost=("Estimated cost", "mean"),
            avg_cost_per_1k_views=("Cost per 1K views", "mean"),
        )
    )

def content_theme_summary(df):
    return (
        df.groupby(["Brand", "Content theme"], as_index=False)
        .agg(
            videos=("Content link", "nunique"),
            creators=("Influencer", "nunique"),
            total_views=("Views", "sum"),
            avg_views=("Views", "mean"),
            avg_engagement=("Engagement rate", "mean"),
        )
        .sort_values(["Brand", "total_views"], ascending=[True, False])
    )

def monthly_summary(df):
    return (
        df.groupby(["Month", "Brand"], as_index=False)
        .agg(
            videos=("Content link", "nunique"),
            creators=("Influencer", "nunique"),
            total_views=("Views", "sum"),
            avg_views=("Views", "mean"),
            avg_engagement=("Engagement rate", "mean"),
            estimated_cost=("Estimated cost", "sum"),
        )
    )

def creator_opportunity_score(df):
    # Screening score, not a prediction of future performance.
    # Uses competitor validation + efficiency + engagement + repeat collaboration.
    c = creator_summary(df).copy()

    # Normalize within the full competitor universe.
    def pct_rank(s):
        return s.rank(pct=True, method="average")

    c["view_score"] = pct_rank(c["avg_views"].clip(lower=0))
    c["engagement_score"] = pct_rank(c["avg_engagement"].clip(lower=0))
    c["efficiency_score"] = pct_rank(c["avg_views_per_1k_subscribers"].clip(lower=0))
    c["repeat_score"] = pct_rank(c["collaborations"])

    c["Opportunity score"] = (
        0.30 * c["view_score"]
        + 0.25 * c["engagement_score"]
        + 0.25 * c["efficiency_score"]
        + 0.20 * c["repeat_score"]
    ) * 100

    # Shared competitors get a validation flag, but are not automatically ranked higher.
    major_creators = set(c.loc[c["Brand"] == "Major Fitness", "Influencer"])
    ritfit_creators = set(c.loc[c["Brand"] == "RITFIT", "Influencer"])
    c["Competitor overlap"] = c["Influencer"].isin(major_creators & ritfit_creators)

    return c.sort_values("Opportunity score", ascending=False)

def main():
    df = load()
    outputs = {
        "competitor_summary.csv": competitor_summary(df),
        "creator_summary.csv": creator_summary(df),
        "creator_overlap.csv": creator_overlap(df),
        "collaboration_type_summary.csv": collaboration_type_summary(df),
        "content_theme_summary.csv": content_theme_summary(df),
        "monthly_summary.csv": monthly_summary(df),
        "creator_opportunity_score.csv": creator_opportunity_score(df),
    }
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for name, table in outputs.items():
        path = PROCESSED_DIR / name
        table.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"Saved {path}")

if __name__ == "__main__":
    main()
