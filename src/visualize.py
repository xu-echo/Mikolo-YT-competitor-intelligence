import pandas as pd
import matplotlib.pyplot as plt
from .config import PROCESSED_DIR, FIGURES_DIR

def save(name):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / name, dpi=180, bbox_inches="tight")
    plt.close()

def main():
    creator = pd.read_csv(PROCESSED_DIR / "creator_summary.csv")
    collab = pd.read_csv(PROCESSED_DIR / "collaboration_type_summary.csv")
    theme = pd.read_csv(PROCESSED_DIR / "content_theme_summary.csv")
    monthly = pd.read_csv(PROCESSED_DIR / "monthly_summary.csv")

    # 1. Creator count
    creator.groupby("Brand")["Influencer"].nunique().plot(kind="bar", figsize=(7,5))
    plt.title("YouTube Creator Count")
    plt.xlabel("Brand"); plt.ylabel("Unique creators")
    save("01_creator_count.png")

    # 2. Collaboration type mix
    pivot = collab.pivot(index="Promotion type", columns="Brand", values="videos").fillna(0)
    pivot.plot(kind="bar", figsize=(8,5))
    plt.title("Collaboration Type Mix")
    plt.xlabel("Promotion type"); plt.ylabel("Videos")
    save("02_collaboration_type_mix.png")

    # 3. Content theme
    pivot = theme.pivot(index="Content theme", columns="Brand", values="videos").fillna(0)
    pivot.sort_values(by=list(pivot.columns), ascending=False).head(12).plot(kind="bar", figsize=(10,6))
    plt.title("Top YouTube Content Themes")
    plt.xlabel("Content theme"); plt.ylabel("Videos")
    save("03_content_theme.png")

    # 4. Creator performance
    top = creator.sort_values("total_views", ascending=False).head(15).copy()
    top["label"] = top["Influencer"] + " (" + top["Brand"] + ")"
    top.set_index("label")["total_views"].sort_values().plot(kind="barh", figsize=(10,7))
    plt.title("Top Creators by Total Views")
    plt.xlabel("Total views"); plt.ylabel("Creator")
    save("04_top_creators_by_views.png")

    # 5. Views vs engagement
    fig, ax = plt.subplots(figsize=(9,6))
    for brand, g in creator.groupby("Brand"):
        ax.scatter(g["avg_views"], g["avg_engagement"], label=brand, alpha=0.75)
    ax.set_xscale("log")
    ax.set_xlabel("Average views (log scale)")
    ax.set_ylabel("Average engagement rate")
    ax.set_title("Creator Performance: Views vs Engagement")
    ax.legend()
    save("05_creator_views_vs_engagement.png")

    # 6. Monthly activity
    for brand, g in monthly.groupby("Brand"):
        ax = g.sort_values("Month").plot(x="Month", y="videos", marker="o", figsize=(10,5), label=brand)
    plt.title("Monthly YouTube Collaboration Activity")
    plt.xlabel("Month"); plt.ylabel("Videos")
    save("06_monthly_activity.png")

if __name__ == "__main__":
    main()
