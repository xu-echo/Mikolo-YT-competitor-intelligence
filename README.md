# MIKOLO YouTube Competitor Intelligence

A Python-based competitive creator intelligence project for **MIKOLO Fitness**.

## Business question

MIKOLO has not yet developed a YouTube creator program. This project analyzes the YouTube content datasets of **Major Fitness** and **RITFIT** to answer:

1. Which YouTube creators are competitors working with?
2. What types of collaborations are they using?
3. What content themes and products are being promoted?
4. Which creators appear repeatedly or perform strongly?
5. Where are the potential creator/content gaps for MIKOLO?

## Analysis framework

**Creator → Collaboration Type → Content Theme → Product/Keyword → Performance → MIKOLO Opportunity**

### Main outputs

- `creator_summary.csv`: creator-level collaboration and performance summary
- `creator_overlap.csv`: creators shared by Major Fitness and RITFIT
- `collaboration_type_summary.csv`: Sponsored / Mentioned / Suspected mix
- `content_theme_summary.csv`: normalized themes from Type + Tags
- `monthly_summary.csv`: monthly competitor activity
- `creator_opportunity_score.csv`: a screening score for MIKOLO creator prospecting
- PNG charts in `reports/figures/`

## Important data interpretation

The source files come from NoxInfluencer brand-monitor data. `Promotion type` is treated as the observed/estimated collaboration signal:

- `Sponsored` = strongest explicit sponsorship signal
- `Mentioned` = product/brand mention signal
- `Suspected` = suspected brand collaboration

This project **does not claim that every "Suspected" row is a confirmed paid collaboration**.

## Run

```bash
pip install -r requirements.txt

python -m src.data_prep
python -m src.analysis
python -m src.visualize
```

Or open:

```text
notebooks/01_mikolo_competitor_analysis.ipynb
```

## Why this matters for MIKOLO

The end goal is not simply to compare views. The analysis is designed to support creator sourcing decisions:

- **Competitor-validated creators**: creators already proven to work with fitness-equipment brands
- **Creator overlap**: creators approached by both competitors
- **Creator gaps**: relevant creator profiles with strong performance but no observed competitor collaboration
- **Collaboration-format gaps**: content formats competitors are underusing
- **Prospecting priorities**: creators ranked using audience size, view efficiency, engagement and repeat collaboration signals

## Data privacy

Before publishing this repository publicly, review whether estimated cost or other commercial intelligence should be kept private.
