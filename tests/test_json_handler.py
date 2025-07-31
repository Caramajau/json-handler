from collections.abc import Callable, Mapping
from typing import Any
from unittest import TestCase, main
from os import path, rmdir, remove, makedirs
from src.json_handler_caramajau.json_handler import JSONHandler


class TestJSONHandler(TestCase):
    def setUp(self) -> None:
        self.__test_file: str = "test_data/test.json"
        self.__test_dir: str = path.dirname(self.__test_file)

    def test_read_json__given_file_not_exists__returns_empty(self) -> None:
        handler: JSONHandler[str] = JSONHandler(self.__test_file)

        result: Mapping[str, str] = handler.read_json()
        self.assertEqual(result, {})

    def test_write_json__given_valid_data_read_json__returns_data(self) -> None:
        data: dict[str, str | int] = {"key": "value", "num": 1337}
        handler: JSONHandler[str | int] = JSONHandler(self.__test_file)

        handler.write_json(data)
        self.assertTrue(path.exists(self.__test_file))

        read_data: Mapping[str, str | int] = handler.read_json()
        self.assertEqual(read_data, data)

    def test_write_json__given_valid_data__creates_directory_and_file(self) -> None:
        # Make sure there is no directory or file
        self.assertFalse(path.exists(self.__test_dir))
        self.assertFalse(path.exists(self.__test_file))

        data: dict[str, int] = {"a": 1}
        handler: JSONHandler[int] = JSONHandler(self.__test_file)

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
