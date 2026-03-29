import shutil
from pathlib import Path
from tqdm import tqdm
from mdutils.mdutils import MdUtils
from pathvalidate import sanitize_filename
from polarsteps_data_parser.model import Trip, Step

class MarkdownGenerator:
    """Generates a Markdown report using mdutils and copies media files."""

    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)

    def generate(self, trip: Trip) -> None:
        """Generate the Markdown file and copy media."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        md_filename = sanitize_filename(trip.name)
        md_file_path = self.output_dir / md_filename

        md = MdUtils(file_name=str(md_file_path), title=trip.name)
        md.new_header(level=1, title=trip.name)

        md.new_paragraph(f"{trip.start_date.strftime('%d.%m.%Y')} - {trip.end_date.strftime('%d.%m.%Y')}")

        if trip.cover_photo_path:
            cover_path = Path(trip.cover_photo_path)
            if cover_path.exists():
                cover_dest_name = f"cover{cover_path.suffix}"
                shutil.copy2(cover_path, self.output_dir / cover_dest_name)
                md.new_line(md.new_inline_image(text="Cover", path=cover_dest_name))

        md.new_line("") # Add some space

        for step in tqdm(trip.steps, desc="Generating Markdown", ncols=80):
            self._add_step(md, step)

        md.create_md_file()

    def _add_step(self, md: MdUtils, step: Step) -> None:
        """Add a single step to the MdUtils object."""
        md.new_header(level=2, title=step.name)

        md.new_paragraph(f"*{step.date.strftime('%d.%m.%Y')}, {step.location.name}, {step.location.country}*")

        if step.description:
            md.new_paragraph(step.description)

        if step.photos or step.videos:
            step_media_rel_folder = sanitize_filename(step.name).replace(" ", "_")
            if not step_media_rel_folder:
                step_media_rel_folder = f"step_{step.step_id}"

            step_media_abs_path = self.output_dir / step_media_rel_folder
            step_media_abs_path.mkdir(parents=True, exist_ok=True)

            for photo in step.photos:
                if photo.exists():
                    shutil.copy2(photo, step_media_abs_path / photo.name)
                    rel_photo_path = f"{step_media_rel_folder}/{photo.name}"
                    md.new_line(md.new_inline_image(text=step.name, path=rel_photo_path))
                    md.new_line("") # Space after image

            for video in step.videos:
                if video.exists():
                    shutil.copy2(video, step_media_abs_path / video.name)
                    rel_video_path = f"{step_media_rel_folder}/{video.name}"
                    md.new_line(f"Video: [{video.name}]({rel_video_path})")

        if step.comments:
            md.new_header(level=3, title="Comments")
            for comment in step.comments:
                md.new_paragraph(f"> **{comment.follower.name}**: {comment.text}")
