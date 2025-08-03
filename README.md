## JSON Handler

### Overview
Code to make it easier to read and write to a JSON file. It provides an abstraction layer, since you don't need to specify the details of how the JSON is read or written (such as file encoding, etc.). This eliminates the ability to customize how the JSON is read or written. However, most instances will probably not require such customization, so this works for most cases.

**NOTE**: The code uses utf-8 encoding only, since it is a very common encoding.

### Usage
To use the JSON handler, create an instance of the `JSONHandler` class and specify the file path in the constructor. You can then read and write to the file using the `read_json` and `write_json` methods.

The class utilizes generics, allowing you to specify the type of data you want to read or write. Make sure the data type is serializable to JSON, since the file will not be created if it is not.

**Note**: Type hints in Python are not enforced at runtime. You are responsible for ensuring that the data you pass matches the expected type and is serializable.

#### Example code
```python
from json_handler_caramajau.json_handler import JSONHandler
from typing import Mapping

handler: JSONHandler[str] = JSONHandler("path/to/your/file")

data: Mapping[str, str] = {"key": "value"}
handler.write_json(data)

read_data: Mapping[str, str] = handler.read_json()
print(read_data)  # Output: {'key': 'value'}
```

### Requirements
- Python 3.12 or higher

### Installation
You can install the package using pip:
```bash
pip install json-handler-caramajau
```
### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contributing
If you want to contribute to this project, feel free to open an issue or a pull request. Contributions are welcome, but since the project is so simple, I expect that there probably won't be many.

### Author
This project is maintained by Caramajau. If you have any questions or suggestions, feel free to reach out.
