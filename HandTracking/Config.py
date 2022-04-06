import json
from json import JSONDecodeError
from typing import Optional, List

from HandTracking.Point import Point


class Config:
    filepath: str = "./config.json"
    empty_config: dict = {
        "startup": {},
        "cal_points": {},
        "bou_points": {}
    }

    @classmethod
    def load(cls) -> Optional[dict]:
        """
        Loads the config JSON file into a dictionary.

        :return: A dictionary symbolizing the config file, or None if it cannot be parsed or doesn't exist
        """
        try:
            with open(cls.filepath, "r") as file:
                return json.load(file)
        except (JSONDecodeError, FileNotFoundError):
            return None

    @classmethod
    def load_calibration_points(cls) -> Optional[List[Point]]:
        """
        Converts calibration points from the config file to a list of Point objects.

        :return: A list of Point objects saved in the config file, or None if it doesn't exist
        """
        try:
            config: Optional[dict] = cls.load()
            point_list: List[Point] = [Point.from_dict(config["cal_points"]["point0"]),
                                       Point.from_dict(config["cal_points"]["point1"]),
                                       Point.from_dict(config["cal_points"]["point2"]),
                                       Point.from_dict(config["cal_points"]["point3"])]
            return point_list
        except (KeyError, TypeError):
            return None

    @classmethod
    def load_boundary_points(cls) -> Optional[List[Point]]:
        """
        Converts boundary points from the config file to a list of Point objects.

        :return: A list of Point objects saved in the config file, or None if it doesn't exist
        """
        try:
            config: Optional[dict] = cls.load()
            point_list: List[Point] = [Point.from_dict(config["bou_points"]["point0"]),
                                       Point.from_dict(config["bou_points"]["point1"])]
            return point_list
        except (KeyError, TypeError):
            return None

    @classmethod
    def load_startup_settings(cls) -> Optional[dict]:
        """
        Reads the config file if it exists and returns the part relevant for startup settings.

        :return: A dictionary containing the startup settings from the config file, None if it doesn't exist
        """
        try:
            return cls.load()["startup"]
        except TypeError:
            return None

    @classmethod
    def save_startup_settings(cls, settings: dict) -> None:
        """
        Writes the new startup settings to the config file.

        :param settings: The dictionary of settings to save
        """
        config = cls.load()

        if not config:
            config = cls.empty_config

        config["startup"] = settings
        cls.__write(config)

    @classmethod
    def save_calibration_points(cls, cal_points: List[Point]) -> None:
        """
        Writes the new calibration points to the config file.

        :param cal_points: A list of Point objects to write to the config file
        """
        config = cls.load()

        if not config:
            config = cls.empty_config

        cal_points = cls.point_list_to_dict(cal_points)
        config["cal_points"] = cal_points
        cls.__write(config)

    @classmethod
    def save_boundary_points(cls, bou_points: List[Point]) -> None:
        """
        Writes the new boundary points to the config file.

        :param bou_points: A list of Point objects to write to the config file
        """
        config = cls.load()

        if not config:
            config = cls.empty_config

        bou_points = cls.point_list_to_dict(bou_points)
        config["bou_points"] = bou_points
        cls.__write(config)

    @classmethod
    def point_list_to_dict(cls, point_list: List[Point]) -> dict:
        """
        Converts a list of Point objects to a dictionary representation.

        :param point_list: The list of Point objects to convert
        :return: A dictionary containing the given points
        """
        dictionary = {}
        for i, point in enumerate(point_list):
            dictionary[f"point{i}"] = point.__dict__

        return dictionary

    @classmethod
    def __write(cls, settings: dict) -> None:
        """
        Writes the given setting configuration to the config file.

        :param settings: The settings to write to the config file
        """
        with open(cls.filepath, "w") as file:
            json.dump(settings, file)
