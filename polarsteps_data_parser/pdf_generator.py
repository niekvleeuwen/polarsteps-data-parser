from reportlab.lib import utils
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from polarsteps_data_parser.model import Trip, Step


class PDFGenerator:
    def __init__(self, output: str):
        self.filename = output

    def generate_pdf(self, trip: Trip):
        self.create_step_pdf(trip.steps[0], self.filename)

    @staticmethod
    def wrap_text(text, max_width, canvas, font, font_size):
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

    def create_step_pdf(self, step: Step, filename: str):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, height - 30, f"Step ID: {step.step_id}")
        c.setFont("Helvetica", 12)

        # Basic Information
        c.drawString(30, height - 60, f"Name: {step.name}")
        y_position = height - 80

        # Description
        description_lines = self.wrap_text(step.description, width - 60, c, "Helvetica", 12)
        c.drawString(30, y_position, "Description:")
        y_position -= 20
        for line in description_lines:
            c.drawString(30, y_position, line)
            y_position -= 20

        # Location and Date
        c.drawString(30, y_position, f"Location: {step.location}")
        y_position -= 20
        c.drawString(30, y_position, f"Date: {step.date}")
        y_position -= 40

        # Photos
        c.drawString(30, y_position, "Photos:")
        y_position -= 20
        for photo in step.photos:
            try:
                image = ImageReader(str(photo))
                img_width, img_height = utils.ImageReader(image).getSize()
                aspect = img_height / float(img_width)
                new_width = 100
                new_height = new_width * aspect
                c.drawImage(
                    image,
                    30,
                    y_position - new_height,
                    width=new_width,
                    height=new_height,
                )
                y_position -= new_height + 20
            except Exception as e:
                print(f"Failed to load image {photo}: {e}")

        # Videos
        c.drawString(30, y_position, "Videos:")
        y_position -= 20
        for video in step.videos:
            c.drawString(30, y_position, str(video))
            y_position -= 20

        # Comments
        c.drawString(30, y_position, "Comments:")
        y_position -= 20
        for comment in step.comments:
            c.drawString(30, y_position, f"Author: {comment.author}")
            y_position -= 20
            comment_lines = self.wrap_text(comment.comment, width - 60, c, "Helvetica", 12)
            for line in comment_lines:
                c.drawString(30, y_position, line)
                y_position -= 20
            c.drawString(30, y_position, f"Date: {comment.date}")
            y_position -= 40

        c.save()
