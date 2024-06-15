from loguru import logger
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from polarsteps_data_parser.model import Trip, Step


class PDFGenerator:
    """Generates a PDF for Polarsteps Trip objects."""

    PHOTO_WIDTH = 250

    def __init__(self, output: str) -> None:
        self.filename = output
        self.canvas = None
        self.y_position = None
        self.width = None
        self.height = None

    def generate_pdf(self, trip: Trip) -> None:
        """Generate a PDF for a given trip."""
        self.canvas = Canvas(self.filename, pagesize=letter)

        no_of_steps = len(trip.steps)
        for i, step in enumerate(trip.steps[:2], start=1):
            logger.debug(f"{i}/{no_of_steps} generating pages for step {step.name}")
            self.create_step_pdf(step)

        self.canvas.save()

    def new_page(self) -> None:
        """Add a new page to the canvas."""
        self.canvas.showPage()
        self.width, self.height = letter
        self.y_position = self.height - 30

    def create_step_pdf(self, step: Step) -> None:
        """Add a step to the canvas."""
        self.new_page()

        # Title
        self.heading(step.name)

        # Basic Information
        self.short_text(f"Location: {step.location.name}, {step.location.country}")
        self.short_text(f"Date: {step.date.strftime('%d-%m-%Y')}")

        # Description
        self.long_text(step.description)

        # Comments
        self.long_text("Comments:")
        for comment in step.comments:
            self.short_text(f"Author: {comment.follower.name}")
            self.long_text(comment.text)

        # Photos
        self.short_text("Photos:")
        for photo in step.photos:
            self.photo(photo)

    def heading(self, text: str) -> None:
        """Add heading to canvas."""
        if self.y_position < 50:
            self.new_page()
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawString(30, self.y_position, text)
        self.y_position -= 30

    def short_text(self, text: str) -> None:
        """Add short text to canvas."""
        if self.y_position < 50:
            self.new_page()
        self.canvas.setFont("Helvetica", 12)
        self.canvas.drawString(30, self.y_position, text)
        self.y_position -= 20

    def long_text(self, text: str) -> None:
        """Add long text to canvas."""
        self.y_position -= 10
        lines = self.wrap_text(text, self.width - 60, self.canvas, "Helvetica", 12)
        for line in lines:
            if self.y_position < 50:
                self.new_page()
                self.canvas.setFont("Helvetica", 12)
            self.canvas.drawString(30, self.y_position, line)
            self.y_position -= 20
        self.y_position -= 20

    def photo(self, photo_path: str) -> None:
        """Add photo to canvas."""
        try:
            image = ImageReader(photo_path)
            img_width, img_height = image.getSize()
            aspect = img_height / float(img_width)
            new_height = self.PHOTO_WIDTH * aspect
            if self.y_position - new_height < 50:
                self.canvas.showPage()
                self.y_position = self.height - 30
            self.canvas.drawImage(
                image,
                30,
                self.y_position - new_height,
                width=self.PHOTO_WIDTH,
                height=new_height,
            )
            self.y_position = self.y_position - new_height - 20
        except Exception as e:
            logger.warning(f"Failed to load image {photo_path}: {e}")

    @staticmethod
    def wrap_text(text: str, max_width: int, canvas: Canvas, font: str, font_size: str) -> list:
        """Wrap text to fit within max_width."""
        canvas.setFont(font, font_size)
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if canvas.stringWidth(test_line) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines
