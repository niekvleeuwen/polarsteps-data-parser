import json
from pathlib import Path

import click
from dotenv import load_dotenv
from loguru import logger

from polarsteps_data_parser.enrich_steps_with_comments import StepCommentsEnricher
from polarsteps_data_parser.parser import Parser
from polarsteps_data_parser.pdf_generator import PDFGenerator


def load_json_from_file(path: Path) -> dict:
    with open(path, "r") as file:
        return json.load(file)


@click.command()
@click.option(
    "--input_folder",
    type=click.Path(exists=True),
    required=True,
    help="""
    The input folder should contain the Polarsteps data export of one (!) trip. Make sure the folder contains
    a `trip.json` and `locations.json`.""",
)
def cli(input_folder):
    load_dotenv()

    input_folder = Path(input_folder)
    trip_data_path = input_folder / "trip.json"
    location_data_path = input_folder / "locations.json"

    if not trip_data_path.exists() or not location_data_path.exists():
        raise FileNotFoundError(f"Path {input_folder} does not contain a Polarsteps data export.")

    trip_data = load_json_from_file(trip_data_path)
    location_data = load_json_from_file(location_data_path)

    parser = Parser()
    logger.info("Starting parsing trip")
    trip = parser.parse_trip(trip_data)

    logger.info("Starting parsing location data")
    parser.parse_locations(location_data)  # TODO use location data :)

    # Enrich trip with comment data
    logger.info("Starting parsing comments")
    step_comment_enricher = StepCommentsEnricher(input_folder)
    trip = step_comment_enricher.enrich(trip)

    logger.info("Generating PDF")
    output_file = "report.pdf"
    pdf_generator = PDFGenerator(output_file)
    pdf_generator.generate_pdf(trip)
    logger.info(f"Generated report ({output_file})")


if __name__ == "__main__":
    cli()
