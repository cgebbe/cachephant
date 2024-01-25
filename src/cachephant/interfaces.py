import dataclasses
import abc
from typing import Callable, Iterable, Any
import pandas as pd


@dataclasses.dataclass
class Request:
    func_name: str
    arg_str: str
    utc_time: float
    hash_str: str

    def get_relative_path(self) -> str:
        return f"{self.func_name}/{self.hash_str}"


class HasherInterface(abc.ABC):
    @abc.abstractmethod
    def hash(self, func: Callable, *args: Any, **kwargs: Any) -> Request:
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
    def remove(self, request: Request):
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
    def remove(self, request: Request):
        pass

    @abc.abstractmethod
    def get_all_requests(self) -> pd.DataFrame:
        pass
