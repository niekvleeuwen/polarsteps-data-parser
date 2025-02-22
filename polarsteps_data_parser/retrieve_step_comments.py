import json
import os
from pathlib import Path

import requests

from polarsteps_data_parser.model import Trip, StepComment

# Define the headers used for the request to polarsteps.com
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-NL,en;q=0.9,nl-NL;q=0.8,nl;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Cookie": "",  # Will be retrieved from environment variables
    "Host": "www.polarsteps.com",
    "Polarsteps-Api-Version": "13",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 "
    "Safari/537.36",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}


class StepCommentsEnricher:
    """Enriches steps with comments retrieved using the Polarsteps API."""

    def __init__(self, path: Path) -> None:
        self.comment_data_path = path / "comments.json"
        headers["Cookie"] = os.getenv("COOKIE")

    def enrich(self, trip: Trip) -> None:
        """Enrich trip data with comments.

        Args:
        ----
            trip: trip data

        """
        comment_data = self.retrieve_comments(trip)
        self.add_comments_to_steps(trip, comment_data)

    def retrieve_comments(self, trip: Trip) -> dict:
        """Retrieve comments from Polarsteps API or local file storage.

        Args:
        ----
            trip: data of the trip

        Returns:
        -------
            dict: comment data

        """
        # Check if there is comment data and give the option to download/use existing data
        if self.comment_data_path.exists():
            comment_data = self.load_comments_from_file()
            return comment_data

        # Retrieve data from the API
        comment_data = {"steps": []}
        for step in trip.steps:
            comments = self.get_comments_for_step(step.step_id)
            comment_data["steps"].append({"id": step.step_id, "comments": comments["comments"]})

        self.write_comments_to_file(comment_data)

        return comment_data

    def write_comments_to_file(self, comment_data: dict) -> None:
        """Write comments data to file.

        Args:
        ----
            comment_data: comment data retrieved from the API

        """
        with open(self.comment_data_path, "w") as file:
            json.dump(comment_data, file, indent=4)

    def load_comments_from_file(self) -> dict:
        """Load comments from data file.

        Returns:
        -------
            dict: comment data

        """
        with open(self.comment_data_path, "r") as file:
            return json.load(file)

    @staticmethod
    def get_comments_for_step(step_id: str) -> dict:
        """Retrieve all comments for a step.

        Args:
        ----
            step_id: id of the step (e.g. 82089888)

        Returns:
        -------
            dict: response parsed to JSON

        """
        url = f"https://www.polarsteps.com/api/social/steps/{step_id}/comments"

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

    @staticmethod
    def add_comments_to_steps(trip: Trip, comment_data: dict) -> Trip:
        """Parse the comment data to the model.

        Args:
        ----
            trip: trip data
            comment_data: comment data

        Returns:
        -------
            trip: trip data including comments

        """
        for step, comments in zip(trip.steps, comment_data["steps"]):
            if step.step_id != comments["id"]:
                raise ValueError("Steps in trip and comment data are not in the same order.")
            step.comments = [StepComment.from_json(c) for c in comments["comments"]]

        return trip
