from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import Self


@dataclass
class Location:
    lat: float
    lon: float
    time: datetime


@dataclass
class Follower:
    user_id: str
    username: str
    first_name: str
    last_name: str

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return Follower(
            user_id=data["id"],
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )


@dataclass
class StepComment:
    comment_id: str
    text: str
    date: str
    user_id: str


@dataclass
class Step:
    step_id: str
    name: str
    description: str
    location: str
    date: date
    photos: list[Path]
    videos: list[Path]
    comments: list[StepComment]


@dataclass
class Trip:
    name: str
    start_date: datetime
    end_date: datetime
    cover_photo_path: str
    steps: list[Step]
