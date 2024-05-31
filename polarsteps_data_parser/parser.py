from datetime import datetime

from polarsteps_data_parser.model import Trip, Step, Location


class Parser:
    def __init__(self):
        pass

    def parse_trip(self, trip_data):
        trip = Trip(
            name=trip_data["name"],
            start_date=self.parse_date(trip_data.get("start_date")),
            end_date=self.parse_date(trip_data.get("end_date")),
            cover_photo_path=trip_data["cover_photo_path"],
            steps=[],
        )

        steps = []

        # Extract steps
        all_steps = trip_data.get("all_steps")
        for step in all_steps:
            steps.append(
                Step(
                    step_id=step["id"],
                    name=step["name"] or step["display_name"],
                    description=step["description"],
                    location=step["location"],
                    date=self.parse_date(step["start_time"]),
                    photos=[],  # TODO
                    videos=[],  # TODO
                    comments=[],
                )
            )

        trip.steps = steps
        return trip

    def parse_locations(self, location_data):
        locations = [
            Location(lat=loc["lat"], lon=loc["lon"], time=self.parse_date(loc["time"]))
            for loc in location_data["locations"]
        ]
        return locations

    def parse_date(self, date: str) -> datetime:
        """Convert a string containing a timestamp to a datetime object."""
        timestamp = float(date)
        date_time = datetime.fromtimestamp(timestamp)
        return date_time
