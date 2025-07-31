from collections.abc import Callable, Mapping
from typing import Any
from unittest import TestCase, main
from os import path, rmdir, remove, makedirs
from src.json_handler_caramajau.json_handler import JSONHandler
from parameterized import parameterized  # type: ignore


class TestJSONHandler(TestCase):
    def setUp(self) -> None:
        self.__test_file: str = "test_data/test.json"
        self.__test_dir: str = path.dirname(self.__test_file)

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

    def test_write_json__given_non_serializable_type__removes_file(self) -> None:
        handler: JSONHandler[Callable[..., Any]] = JSONHandler(self.__test_file)
        data: dict[str, Callable[..., Any]] = {"func": lambda x: x}  # type: ignore
        handler.write_json(data)
        self.assertFalse(path.exists(self.__test_file))

    def tearDown(self) -> None:
        self.__clean_up_test_environment()

    def __clean_up_test_environment(self) -> None:
        if path.exists(self.__test_file):
            remove(self.__test_file)
        if path.exists(self.__test_dir):
            rmdir(self.__test_dir)


if __name__ == "__main__":
    main()
