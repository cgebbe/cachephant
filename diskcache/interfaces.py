import dataclasses
import abc
import fsspec
from typing import Callable, Iterable, Any
from pathlib import PurePosixPath

fs = fsspec.filesystem("s3")

import datetime


@dataclasses.dataclass
class Request:
    func: Callable
    args: Any
    kwargs: Any
    time: datetime.datetime
    hash_str: str = ""

    def get_relative_path() -> PurePosixPath:
        raise NotImplementedError


@abc.ABC
class HasherInterface:
    @abc.abstractmethod
    def hash(request: Request) -> str:
        pass


@dataclasses.dataclass
class Response:
    result: Any
    file_size_in_bytes: int


@abc.ABC
class StorageInterface:
    @abc.abstractmethod
    def save(request: Request, response: Response):
        pass

    @abc.abstractmethod
    def load(request: Request):
        pass

    @abc.abstractmethod
    def remove(request: Request):
        pass


@abc.ABC
class DatabaseInterface(StorageInterface):
    @abc.abstractmethod
    def get_all_requests() -> Iterable[Request]:
        pass
