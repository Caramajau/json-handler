from collections.abc import Callable, Mapping
from shutil import rmtree
from typing import Any, Final
from unittest import TestCase, main
from os import path, makedirs, remove
from src.json_handler_caramajau.json_handler import JSONHandler
from parameterized import parameterized  # type: ignore


class TestJSONHandler(TestCase):
    __test_dir: Final[str] = "test_data"
    __test_file_name: Final[str] = "test.json"
    __test_file: Final[str] = path.join(__test_dir, __test_file_name)

    def setUp(self) -> None:
        # Keep track of files created outside of the test_data directory
        self.__created_files: list[str] = []

    def test_read_json__given_file_not_exists__returns_empty(self) -> None:
        handler: JSONHandler[str] = JSONHandler(self.__test_file)

        result: Mapping[str, str] = handler.read_json()
        self.assertEqual(result, {})

    # Expand had to be used with unittest
    @parameterized.expand(  # type: ignore
        [
            ({"dict": {}},),
            ({"list": []},),
            ({"str": "hello"},),
            ({"int": 1},),
            ({"float": 0.1},),
            ({"bool": True},),
            ({"none": None},),
        ]
    )
    def test_write_json__given_serializable_type_read_json__returns_data(
        self, data: Mapping[str, Any]
    ) -> None:
        handler: JSONHandler[Any] = JSONHandler(self.__test_file)

        handler.write_json(data)
        self.assertTrue(path.exists(self.__test_file))

        read_data: Mapping[str, Any] = handler.read_json()
        self.assertEqual(read_data, data)

    @parameterized.expand(  # type: ignore
        [
            ({"dict": {}},),
            ({"list": []},),
            ({"str": "hello"},),
            ({"int": 1},),
            ({"float": 0.1},),
            ({"bool": True},),
            ({"none": None},),
        ]
    )
    def test_write_json_given_serializable_type__creates_directory_and_file(
        self, data: Mapping[str, Any]
    ) -> None:
        # Make sure there is no directory or file
        self.assertFalse(path.exists(self.__test_dir))
        self.assertFalse(path.exists(self.__test_file))

        handler: JSONHandler[Any] = JSONHandler(self.__test_file)

        handler.write_json(data)
        self.assertTrue(path.exists(self.__test_dir))
        self.assertTrue(path.exists(self.__test_file))

    def test_read_json__given_invalid_json__returns_empty(self) -> None:
        self.__write_custom_json("{invalid json}")
        handler: JSONHandler[str] = JSONHandler(self.__test_file)

        result: Mapping[str, str] = handler.read_json()
        self.assertEqual(result, {})

    def __write_custom_json(self, content: str) -> None:
        makedirs(self.__test_dir, exist_ok=True)
        with open(self.__test_file, "w", encoding="utf-8") as f:
            f.write(content)

    @parameterized.expand(  # type: ignore
        [
            ("test", __test_file_name),
            (__test_file_name, __test_file_name),
        ]
    )
    def test_write_json__given_only_file_name__creates_file_in_current_directory(
        self, test_file: str, expected_file: str
    ) -> None:
        handler: JSONHandler[str] = JSONHandler(test_file)
        data: Mapping[str, str] = {"key": "value"}

        handler.write_json(data)
        self.assertTrue(path.exists(expected_file))
        self.__track_file(expected_file)

    def __track_file(self, file_path: str) -> None:
        if file_path not in self.__created_files:
            self.__created_files.append(file_path)

    @parameterized.expand(  # type: ignore
        [
            (path.join(__test_dir, "test"), __test_file),
            (__test_file, __test_file),
        ]
    )
    def test_write_json__given_file_and_directory__creates_file_in_directory(
        self, test_file: str, expected_file: str
    ) -> None:
        handler: JSONHandler[str] = JSONHandler(test_file)
        data: Mapping[str, str] = {"key": "value"}

        handler.write_json(data)
        self.assertTrue(path.exists(expected_file))

    def test_write_json__given_non_serializable_type__removes_file(self) -> None:
        handler: JSONHandler[Callable[..., Any]] = JSONHandler(self.__test_file)
        data: dict[str, Callable[..., Any]] = {"func": lambda x: x}  # type: ignore
        handler.write_json(data)
        self.assertFalse(path.exists(self.__test_file))

    def tearDown(self) -> None:
        self.__clean_up_created_files()
        self.__clean_up_test_data_directory()

    def __clean_up_created_files(self) -> None:
        for file_path in self.__created_files:
            if path.exists(file_path):
                remove(file_path)

    def __clean_up_test_data_directory(self) -> None:
        if path.exists(self.__test_dir):
            rmtree(self.__test_dir)

if __name__ == "__main__":
    main()
