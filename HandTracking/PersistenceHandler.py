import json
from json import JSONDecodeError
from typing import Optional

from HandTracking.Config import Config
from HandTracking.JsonHandler import JsonHandler
from HandTracking.Point import Point


class PersistenceHandler:
    filepath: str = "./drawing.json"
    file_handler = JsonHandler(filepath)

    @classmethod
    def load(cls) -> Optional[dict]:
        """
        Loads the drawing JSON file into a dictionary.

        :return: A dictionary symbolizing the saved drawing, or None if it cannot be parsed or doesn't exist
        """
        try:
            with open(cls.filepath, "r") as file:
                return json.load(file)
        except (JSONDecodeError, FileNotFoundError):
            return None

    @classmethod
    def __write(cls, drawing: dict) -> None:
        """
        Writes the given drawing a JSON file.

        :param drawing: The drawing to write to a JSON file
        """
        with open(cls.filepath, "w") as file:
            json.dump(drawing, file)

    @classmethod
    def save_drawing(cls, lines: list[tuple[list[int], list[Point]]]) -> None:
        drawing: dict = {}

        for i, line in enumerate(lines):
            drawing[f"line{i}"] = PersistenceHandler.__line_tuple_to_dict(line)

        PersistenceHandler.__write(drawing)

    @classmethod
    def __color_list_to_dict(cls, color_list: list[int]) -> dict:
        return {"b": color_list[0], "g": color_list[1], "r": color_list[2]}

    @classmethod
    def __line_tuple_to_dict(cls, line_tuple: tuple) -> dict:
        return {"color": PersistenceHandler.__color_list_to_dict(line_tuple[0]),
                "points": Config.point_list_to_dict(line_tuple[1])}
