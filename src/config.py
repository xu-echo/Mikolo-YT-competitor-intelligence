from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "reports" / "figures"

MAJOR_FILE = RAW_DIR / "major_fitness_youtube.xlsx"
RITFIT_FILE = RAW_DIR / "ritfit_youtube.csv"
