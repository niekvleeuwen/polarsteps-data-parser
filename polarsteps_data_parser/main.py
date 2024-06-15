from pathlib import Path

import click
from dotenv import load_dotenv
from loguru import logger

from polarsteps_data_parser.retrieve_step_comments import StepCommentsEnricher
from polarsteps_data_parser.model import Trip, Location
from polarsteps_data_parser.pdf_generator import PDFGenerator
from polarsteps_data_parser.utils import load_json_from_file


@click.command()
@click.option(
    "--input-folder",
    type=click.Path(exists=True),
    required=True,
    help="""
    The input folder should contain the Polarsteps data export of one (!) trip. Make sure the folder contains
    a `trip.json` and `locations.json`.""",
)
@click.option(
    "--enrich-comments",
    is_flag=True,
    show_default=True,
    default=False,
    help="Whether to enrich the trip with comments or not.",
)
def cli(input_folder: str, enrich_comments: str) -> None:
    """Entry point for the application."""
    load_dotenv()

    input_folder = Path(input_folder)
    trip_data_path = input_folder / "trip.json"
    location_data_path = input_folder / "locations.json"

    if not trip_data_path.exists() or not location_data_path.exists():
        raise FileNotFoundError(f"Path {input_folder} does not contain a Polarsteps data export.")

    trip_data = load_json_from_file(trip_data_path)
    location_data = load_json_from_file(location_data_path)

    logger.info("Starting parsing trip")
    trip = Trip.from_json(trip_data)

    if enrich_comments is True:
        logger.info("Starting parsing comments")
        StepCommentsEnricher(input_folder).enrich(trip)

    logger.info("Starting parsing location data")
    [Location.from_json(data) for data in location_data["locations"]]  # TODO! use location data

    logger.info("Generating PDF")
    output_file = "report.pdf"  # TODO! make configurable
    pdf_generator = PDFGenerator(output_file)
    pdf_generator.generate_pdf(trip)
    logger.info(f"Generated report ({output_file})")


if __name__ == "__main__":
    cli()
