from cachephant.interfaces import (
    Request,
    Response,
    FileSystemInterface,
    NoRequestFoundError,
)
from typing import Any
import pickle  # NOTE: Maybe use hickle instead?
import fsspec.implementations.local
import functools


class FileSystem(FileSystemInterface):
    def __init__(self, prefix: str, protocol="file", **storage_options) -> None:
        self.fs: fsspec.AbstractFileSystem = fsspec.filesystem(
            protocol, **storage_options
        )
        self.prefix = str(prefix)

    def save(self, request: Request, result: Any) -> Response:
        path = self._get_absolute_path(request)
        self.fs.mkdir(self.fs._parent(path), create_parents=True)
        with self.fs.open(path, "wb") as f:
            pickle.dump(result, f)
        return self.construct_response(request, result)

    def load(self, request: Request) -> Response:
        path = self._get_absolute_path(request)
        try:
            with self.fs.open(path, "rb") as f:
                result = pickle.load(f)
        except FileNotFoundError as err:
            raise NoRequestFoundError from err
        else:
            return self.construct_response(request, result)

    def remove(self, request: Request):
        path = self._get_absolute_path(request)
        # FIXME: Shall we also delete any parents
        self.fs.rm(path)

    # @functools.lru_cache() # request is an unhashable type...
    def _get_absolute_path(self, request: Request) -> str:
        return self.fs.sep.join(
            [self.prefix, request.func_name, request.hash_str + ".pickle"]
        )

    def construct_response(self, request: Request, result: Any) -> Response:
        path = self._get_absolute_path(request)
        file_size = self.fs.info(path)["size"]
        return Response(result=result, file_size_in_bytes=file_size)
