import abc
import dataclasses
from collections.abc import Callable
from typing import Any

import pandas as pd
from beardataclass import BearDataClass


class NoRequestFoundError(ValueError):
    pass


@dataclasses.dataclass
class Request(BearDataClass):
    hash_str: str
    func_name: str
    arg_str: str
    utc_time: float

    def get_relative_path(self) -> str:
        return f"{self.func_name}/{self.hash_str}"


class HasherInterface(abc.ABC):
    @abc.abstractmethod
    def hash_func(self, func: Callable, *args: Any, **kwargs: Any) -> Request:
        pass


@dataclasses.dataclass
class Response:
    result: Any
    file_size_in_bytes: int


class FileSystemInterface(abc.ABC):
    @abc.abstractmethod
    def save(self, request: Request, result: Any) -> Response:
        pass

    @abc.abstractmethod
    def load(self, request: Request) -> Response:
        pass

    @abc.abstractmethod
    def remove(self, request: Request) -> None:
        pass


class DatabaseInterface(abc.ABC):
    @abc.abstractmethod
    def save(self, request: Request, response: Response) -> None:
        pass

    @abc.abstractmethod
    def load(self, request: Request) -> None:
        # This shall be used for updating!
        pass

    @abc.abstractmethod
    def remove(self, request: Request) -> None:
        pass

    @abc.abstractmethod
    def get_requests(self, filter_dict: dict | None = None) -> pd.DataFrame:
        pass
