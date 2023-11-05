# Used to simulate a Conf object from grott
from typing import Any, Dict, Union


class FakeConf:
    def __init__(self) -> None:
        self.recorddict: Dict[str, Any] = {}
        self.layout = ""
        self.extvar: Dict[str, Union[str, int, bool]] = {}
        self.verbose = True
