from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"

OWID_PATH = RAW_DATA_DIR / "owid-covid-data.csv.gz"
WORLD_BANK_PATH = RAW_DATA_DIR / "world_bank_health_spending.csv"
METADATA_PATH = RAW_DATA_DIR / "world_bank_country_metadata.csv"
PROCESSED_PATH = PROCESSED_DATA_DIR / "global_health_equity.csv"


def ensure_output_directories() -> None:
    """Create generated-data and output directories when required."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

