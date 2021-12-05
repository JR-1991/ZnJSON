from znconv.config import config
import json
from typing import Any


class ZnEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        for converter in config.ACTIVE_CONVERTER:
            if converter() == o:
                return converter().encode(o)
        raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


class ZnDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.object_hook)

    def object_hook(self, obj):
        try:
            instance = obj["_type"]
        except KeyError:
            return obj

        for converter in config.ACTIVE_CONVERTER:
            if converter.representation == instance:
                return converter().decode(obj)
        raise TypeError(f"Object of type {instance} could not be converted")


if __name__ == "__main__":
    import znconv
    import numpy as np

    znconv.register(znconv.converter.NumpyConverter)

    data = np.arange(10)

    print(json.dumps({"a": 5, "b": data}, cls=ZnEncoder))
    data_str = json.dumps({"a": 5, "b": data}, cls=ZnEncoder)
    print(json.loads(data_str, cls=ZnDecoder))
