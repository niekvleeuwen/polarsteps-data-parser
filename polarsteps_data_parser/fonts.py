import requests
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from polarsteps_data_parser.utils import log

# URL to download the Inter font files
INTER_FONT_URL = "https://github.com/google/fonts/raw/refs/heads/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf?raw=true"

FONT_DIR = Path("fonts")
FONT_PATH = FONT_DIR / "Inter.ttf"


def download_font() -> None:
    """Downloads the Inter font files from the provided URL."""
    # Create font directory if it doesn't exist
    if not FONT_DIR.exists():
        FONT_DIR.mkdir(parents=True)

    # Fetch the Inter font file
    print(f"Downloading font from {INTER_FONT_URL}...")
    response = requests.get(INTER_FONT_URL)

    # Save the font file to disk
    with open(FONT_PATH, "wb") as file:
        file.write(response.content)

    print(f"Font downloaded and saved to {FONT_PATH}")


def register_inter_fonts() -> None:
    """Registers the Inter font with ReportLab. Downloads and saves the font if not already present."""
    # Check if the font files already exist, if not, download them
    if not FONT_PATH.exists():
        download_font()

    # Register the Inter font with ReportLab
    pdfmetrics.registerFont(TTFont("Inter", FONT_PATH))
    log("Inter font registered successfully.")


def get_font_or_fallback(font_name: str, fallback_name: str = "Helvetica") -> str:
    """Returns the font name if registered, otherwise returns fallback font name.

    Args:
        font_name (str): Desired font name (e.g., "Inter", "Inter-Bold").
        fallback_name (str): Fallback font name (default is "Helvetica").

    Returns:
        str: The available font name to use.
    """
    # Ensure the Inter font is registered
    register_inter_fonts()

    # Check if the desired font is available
    registered_fonts = pdfmetrics.getRegisteredFontNames()
    if font_name in registered_fonts:
        return font_name
    else:
        return fallback_name
