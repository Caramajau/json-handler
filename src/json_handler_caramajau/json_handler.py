from json import load, dump, JSONDecodeError
from os import path, makedirs, remove
from collections.abc import Mapping


class JSONHandler[T]:
    """Class to make it easier to read and write to a JSON file.
    If a non-serializable type is given, then the JSON file will not be created.
    """

    def __init__(self, file_path: str) -> None:
        """Initialize the JSON handler with the specified file path.
        Can be relative or absolute, and can be without the .json extension.
        If the file path does not end with .json, it will be added automatically.
        A ValueError will be raised if the file path is empty.

        Args:
            file_path (str): The path to the JSON file. Can be relative or absolute.
        Raises:
            ValueError: If the file path is empty.
        """
        if not file_path:
            raise ValueError("File path cannot be empty.")

        self.__file_path: str = (
            file_path if path.isabs(file_path) else path.abspath(file_path)
        )

        if not self.__file_path.endswith(".json"):
            self.__file_path += ".json"

    def read_json(self) -> Mapping[str, T]:
        """Read JSON data from the file with utf-8 encoding."""
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
        """Write JSON data to the file with utf-8 encoding, creating the file if it does not exist.
        If the data is not serializable or an OSError occurs, the file will not be created.

        Args:
            data (Mapping[str, T]): The data to write to the JSON file.
        """
        try:
            directory: str = path.dirname(self.__file_path)
            if not path.exists(directory):
                print(f"Creating file at {self.__file_path} \n")
                makedirs(directory)

            with open(self.__file_path, "w", encoding="utf-8") as file:
                dump(data, file, indent=4)

        except TypeError as e:
            print(f"Serialization error occurred: {e}")
            self.__remove_file()

        except OSError as e:
            print(f"File operation error occurred: {e}")
            self.__remove_file()

    def __remove_file(self) -> None:
        if path.exists(self.__file_path):
            print("Removing file")
            remove(self.__file_path)
