from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

from polarsteps_data_parser.model import Trip, Step
from tqdm import tqdm


class PDFGenerator:
    """Generates a PDF for Polarsteps Trip objects."""

    MAIN_FONT = ("Helvetica", 12)
    BOLD_FONT = ("Helvetica-Bold", 12)
    HEADING_FONT = ("Helvetica-Bold", 16)
    TITLE_HEADING_FONT = ("Helvetica-Bold", 36)

    def __init__(self, output: str) -> None:
        self.filename = output
        self.canvas = None
        self.width, self.height = letter
        self.y_position = self.height - 30

    def generate_pdf(self, trip: Trip) -> None:
        """Generate a PDF for a given trip."""
        self.canvas = Canvas(self.filename, pagesize=letter)

        self.canvas.setTitle(trip.name)

        self.generate_title_page(trip)

        for i, step in tqdm(enumerate(trip.steps), desc="Generating pages", total=len(trip.steps), ncols=80):
            if i == 5:
                break
            self.generate_step_pages(step)

        self.canvas.save()

    def generate_title_page(self, trip: Trip) -> None:
        """Generate title page."""
        self.title_heading(trip.name)
        self.y_position -= 20
        self.short_text(
            f"{trip.start_date.strftime('%d-%m-%Y')} - {trip.end_date.strftime('%d-%m-%Y')}", bold=True, centered=True
        )
        self.photo(trip.cover_photo_path, centered=True, photo_width=400)

    def generate_step_pages(self, step: Step) -> None:
        """Add a step to the canvas."""
        self.new_page()

        self.heading(step.name)

        self.short_text(f"Location: {step.location.name}, {step.location.country}")
        self.short_text(f"Date: {step.date.strftime('%d-%m-%Y')}")

        self.long_text(step.description)

        for comment in step.comments:
            self.short_text(comment.follower.name, bold=True)
            self.long_text(comment.text)

        for photo in step.photos:
            self.photo(photo)

    def new_page(self) -> None:
        """Add a new page to the canvas."""
        self.canvas.showPage()
        self.width, self.height = letter
        self.y_position = self.height - 30

    def heading(self, text: str) -> None:
        """Add heading to canvas."""
        if self.y_position < 50:
            self.new_page()
        self.canvas.setFont(*self.HEADING_FONT)
        self.canvas.drawString(30, self.y_position, text)
        self.y_position -= 30

    def title_heading(self, text: str) -> None:
        """Add heading to canvas."""
        self.y_position -= 100
        self.canvas.setFont(*self.TITLE_HEADING_FONT)
        self.canvas.drawString(self.calc_width_centered(text, self.TITLE_HEADING_FONT), self.y_position, text)
        self.y_position -= 30

    def calc_width_centered(self, text: str, font: tuple) -> float:
        """Calculate the width location to center the text."""
        return (self.width - stringWidth(text, *font)) / 2.0

    def short_text(self, text: str, bold: bool = False, centered: bool = False) -> None:
        """Add short text to canvas."""
        if self.y_position < 50:
            self.new_page()
        font = self.BOLD_FONT if bold else self.MAIN_FONT
        self.canvas.setFont(*font)
        width = self.calc_width_centered(text, self.MAIN_FONT) if centered else 30
        self.canvas.drawString(width, self.y_position, text)
        self.y_position -= 20

    def long_text(self, text: str) -> None:
        """Add long text to canvas."""
        if text is None:
            return

        self.y_position -= 10
        lines = self.wrap_text(text, self.width - 60)
        for line in lines:
            if self.y_position < 50:
                self.new_page()
                self.canvas.setFont(*self.MAIN_FONT)
            self.canvas.drawString(30, self.y_position, line)
            self.y_position -= 20
        self.y_position -= 20

    def photo(self, photo_path: Path | str, centered: bool = False, photo_width: int = 250) -> None:
        """Add photo to canvas."""
        image = ImageReader(photo_path)
        img_width, img_height = image.getSize()
        aspect = img_height / float(img_width)
        new_height = photo_width * aspect
        if self.y_position - new_height < 50:
            self.canvas.showPage()
            self.y_position = self.height - 30
        self.canvas.drawImage(
            image,
            (self.width - photo_width) / 2.0 if centered else 30,
            self.y_position - new_height,
            width=photo_width,
            height=new_height,
        )
        self.y_position = self.y_position - new_height - 20

    def wrap_text(self, text: str, max_width: int) -> list:
        """Wrap text to fit within max_width."""
        self.canvas.setFont(*self.MAIN_FONT)
        lines = []
        words = text.replace("\n", " <newline> ").split()
        current_line = ""
        for word in words:
            if word == "<newline>":
                lines.append(current_line)
                current_line = ""
                continue

            test_line = f"{current_line} {word}".strip()
            if self.canvas.stringWidth(test_line) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines
