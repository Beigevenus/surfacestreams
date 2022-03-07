import json
from typing import Optional

from HandTracking.Point import Point


class Config:
    filepath: str = "./config.json"
    empty_config: dict = {
        "startup": {},
        "cal_points": {}
    }

    @classmethod
    def load(cls) -> dict:
        with open(cls.filepath, "r") as file:
            return json.load(file)

    @classmethod
    def load_calibration_points(cls) -> Optional[list[Point]]:
        try:
            config: dict = cls.load()
            point_list: list[Point] = [Point.from_dict(config["cal_points"]["point0"]),
                                       Point.from_dict(config["cal_points"]["point1"]),
                                       Point.from_dict(config["cal_points"]["point2"]),
                                       Point.from_dict(config["cal_points"]["point3"]), ]
            return point_list
        except FileNotFoundError:
            return None
        except KeyError:
            return None

    @classmethod
    def save_startup_settings(cls, settings: dict) -> None:
        try:
            config = cls.load()
        except FileNotFoundError:
            config = cls.empty_config

        config["startup"] = settings
        cls.__write(config)

    @classmethod
    def save_calibration_points(cls, cal_points: list[Point]) -> None:
        try:
            config = cls.load()
        except FileNotFoundError:
            config = cls.empty_config

        cal_points = cls.point_list_to_dict(cal_points)
        config["cal_points"] = cal_points
        cls.__write(config)

    @classmethod
    def point_list_to_dict(cls, point_list: list[Point]) -> dict:
        dictionary = {}
        for i, point in enumerate(point_list):
            dictionary[f"point{i}"] = point.__dict__

        return dictionary

    @classmethod
    def __write(cls, settings: dict) -> None:
        with open(cls.filepath, "w") as file:
            json.dump(settings, file)
