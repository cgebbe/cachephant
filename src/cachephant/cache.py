from cachephant.interfaces import (
    HasherInterface,
    FileSystemInterface,
    DatabaseInterface,
    NoRequestFoundError,
    Request,
    Response,
)
import functools
import dataclasses
from typing import Any
import logging

_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class Cache:
    hasher: HasherInterface
    fs: FileSystemInterface
    db: DatabaseInterface

    def __call__(self, func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            request = self.hasher.hash(func, *args, **kwargs)

            try:
                response = self._load(request)
            except NoRequestFoundError:
                print("===my cache miss ===")
                _LOGGER.info("cache miss")
                result = func(*args, **kwargs)
                response = self._save(request, result)
            else:
                _LOGGER.info("cache hit")

            return response.result

        return new_func

    def _save(self, request: Request, result: Any) -> Response:
        response = self.fs.save(request, result)
        self.db.save(request, response)
        return response

    def _load(self, request: Request) -> Response:
        self.db.load(request)
        return self.fs.load(request)

    def _evict(self):
        requests = self.db.get_requests()
        requests_to_evict = requests  # FIXME: A more complicated logic
        for r in requests_to_evict:
            self.db.remove(r)
            self.fs.remove(r)
