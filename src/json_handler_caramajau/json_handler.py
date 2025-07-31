from json import load, dump, JSONDecodeError
from os import path, makedirs
from typing import Mapping


class JSONHandler[T]:
    def __init__(self, file_path: str) -> None:
        self.__file_path: str = file_path

    def read_json(self) -> Mapping[str, T]:
        """Read JSON data from the file."""
        if not path.exists(self.__file_path):
            print(f"File not found at path {self.__file_path}")
            return {}
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                return load(file)
        except JSONDecodeError as e:
            print(f"JSON decoding error occurred: {e}")
            return {}

    def write_json(self, data: Mapping[str, T]) -> None:
        """Write JSON data to the file, creating the file if it does not exist."""
        try:
            directory: str = path.dirname(self.__file_path)
            if not path.exists(directory):
                print(f"Creating file at {self.__file_path} \n")
                makedirs(directory)

            with open(self.__file_path, "w", encoding="utf-8") as file:
                dump(data, file, indent=4)
        except TypeError as e:
            print(f"Serialization error occurred: {e}")
        except OSError as e:
            print(f"File operation error occurred: {e}")
