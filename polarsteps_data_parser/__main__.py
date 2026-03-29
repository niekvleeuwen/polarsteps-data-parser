from pathlib import Path

import click
from dotenv import load_dotenv
from pathvalidate import sanitize_filename
from polarsteps_data_parser.retrieve_step_comments import StepCommentsEnricher
from polarsteps_data_parser.model import Trip, Location
from polarsteps_data_parser.pdf_generator import PDFGenerator
from polarsteps_data_parser.md_generator import MarkdownGenerator
from polarsteps_data_parser.utils import load_json_from_file, log


@click.command()
@click.argument(
    "input-folder",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, readable=True),
)
@click.option(
    "--output",
    default="Trip report.pdf",
    show_default=True,
    help="Output PDF file name (only used if format is pdf)",
)
@click.option(
    "--format",
    type=click.Choice(["pdf", "md"], case_sensitive=False),
    default="pdf",
    show_default=True,
    help="Output format (PDF, or Markdown)",
)
@click.option(
    "--enrich-with-comments",
    is_flag=True,
    show_default=True,
    default=False,
    help="Whether to enrich the trip with comments or not.",
)
def cli(input_folder: str, output: str, format: str, enrich_with_comments: bool) -> None:
    """Parse the data from a Polarsteps trip export.

    INPUT_FOLDER should contain the Polarsteps data export of one (!) trip. Make sure the folder contains
    a `trip.json` and `locations.json`.
    """
    load_dotenv()

    input_folder = Path(input_folder)
    trip_data_path = input_folder / "trip.json"
    location_data_path = input_folder / "locations.json"

    if not trip_data_path.exists() or not location_data_path.exists():
        log("Error: Cannot find Polarsteps trip in folder!")
        log("Please make sure the input folder contains a `trip.json` and a `locations.json` file. ")
        return

    log("✅  Found Polarsteps trip", color="green", bold=True)
    trip_data = load_json_from_file(trip_data_path)
    location_data = load_json_from_file(location_data_path)

    log("🔄 Starting to parse trip...", color="cyan")
    trip = Trip.from_json(trip_data)

    if enrich_with_comments is True:
        StepCommentsEnricher(input_folder).enrich(trip)

    if "locations" in location_data:
        [Location.from_json(data) for data in location_data["locations"]]  # TODO! use location data

    if format in ["pdf"]:
        log("🔄 Generating PDF...", color="cyan")
        pdf_generator = PDFGenerator(output)
        pdf_generator.generate_pdf(trip)
        log(f"✅  Generated report: {click.format_filename(output)}", color="green", bold=True)

    if format in ["md"]:
        log("🔄 Generating Markdown...", color="cyan")
        output_dir = Path(sanitize_filename(trip.name))
        md_generator = MarkdownGenerator(output_dir)
        md_generator.generate(trip)
        log(f"✅  Generated Markdown in folder: {output_dir}", color="green", bold=True)


if __name__ == "__main__":
    load_dotenv()

    cli()
