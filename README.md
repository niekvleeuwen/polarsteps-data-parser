# Polarsteps Data Parser

Tool designed to parse and extract data from the travel tracking app [Polarsteps](https://www.polarsteps.com/) data export. This tool serves two primary purposes:

1. **Data backup**: The data export does not support viewing your data in any useful way. To preserve the data (who knows if Polarsteps still exists in 20 years), the tool combines the data and generates a PDF document.
2. **Data analysis & visualization**: The parsed data can also be leveraged for in-depth analysis, enabling users to gain insights into their travel patterns, destinations visited, duration of stays, distances traveled, and more. This opens up possibilities for statistical analysis, trend identification, and visualization of the trip data (this is still work-in-progess).

## Detailed Usage Guide

If you’re new to Python or command-line tools, I’ve created a step-by-step usage guide to help you install and run polarsteps-data-parser (no programming experience required).

👉 Read the guide here: [Usage guide](https://github.com/niekvleeuwen/polarsteps-data-parser/blob/main/USAGE_GUIDE.md)

## Getting started


1. Clone the repository and navigate to the project root:

```shell
git clone https://github.com/niekvleeuwen/polarsteps-data-parser.git
cd polarsteps-data-parser
```

2. Install dependencies using [uv](https://docs.astral.sh/uv/).
   Make sure `uv` is installed on your system before proceeding.

```shell
uv sync
```

### Usage
To get the following output, run `uv run polarsteps-data-parser --help`.

```shell
Usage: polarsteps-data-parser [OPTIONS] INPUT_FOLDER

  Parse the data from a Polarsteps trip export.

  INPUT_FOLDER should contain the Polarsteps data export of one (!) trip. Make
  sure the folder contains a `trip.json` and `locations.json`.

Options:
  --output TEXT           Output PDF file name  [default: Trip report.pdf]
  --enrich-with-comments  Whether to enrich the trip with comments or not.
  --help                  Show this message and exit.
```

For example, to load and analyse a trip with the data located in the `./data/trip1` folder and enrich the trip with comments, use the following command:

```shell
uv run polarsteps-data-parser ./data/trip1 --enrich-with-comments
```

## Disclaimer
This project is an independent initiative and is in no way affiliated with Polarsteps. All trademarks, service marks, trade names, product names, and logos appearing in this repository are the property of their respective owners, including Polarsteps. The use of these names, logos, and brands is for identification purposes only and does not imply endorsement or affiliation.
