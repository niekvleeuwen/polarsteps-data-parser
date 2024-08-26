# Polarsteps Data Parser

Tool designed to parse and extract data from the travel tracking app [Polarsteps](https://www.polarsteps.com/) data export. This tool serves two primary purposes:

1. **Data backup**: The data export does not support viewing your data in any useful way. To preserve the data (who knows if Polarsteps still exists in 20 years), the tool combines the data and generates a PDF document.
2. **Data analysis & visualization**: The parsed data can also be leveraged for in-depth analysis, enabling users to gain insights into their travel patterns, destinations visited, duration of stays, distances traveled, and more. This opens up possibilities for statistical analysis, trend identification, and visualization of the trip data.

## Getting started

### Installation
To set up the project, ensure you have Python 3.11+ installed. Follow these steps:

Clone the repository:

```shell
git clone https://github.com/niekvleeuwen/polarsteps-data-parser.git
cd polarsteps-trip-analyzer
```

Ensure poetry is available, e.g. on Ubuntu/Debian you can run the following:

```shell
apt-get install python3 poetry
```

Install dependencies using Poetry:

```shell
poetry install
```

Then enter the created virtual environment:

```shell
poetry shell
```

### Usage
To run the project, use the following command:

```shell
polarsteps-data-parser [OPTIONS]
```

For example, to load and analyse a trip with the data located in the `./data/trip1` folder and enrich the trip with comments, use the following command:

```shell
polarsteps-data-parser --input-folder ./data/trip1 --enrich-comments
```

## Disclaimer
This project is an independent initiative and is in no way affiliated with Polarsteps. All trademarks, service marks, trade names, product names, and logos appearing in this repository are the property of their respective owners, including Polarsteps. The use of these names, logos, and brands is for identification purposes only and does not imply endorsement or affiliation.
