import dataclasses
import functools
import logging
from typing import Any

from cachephant.interfaces import (
    DatabaseInterface,
    EvictorInterface,
    FileSystemInterface,
    HasherInterface,
    NoRequestFoundError,
    Request,
    Response,
)

_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class Cache:
    hasher: HasherInterface
    fs: FileSystemInterface
    db: DatabaseInterface
    evictor: EvictorInterface

    def __call__(self, func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            request = self.hasher.hash_func(func, *args, **kwargs)

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
        self._evict()
        response = self.fs.save(request, result)
        self.db.save(request, response)
        return response

    def _load(self, request: Request) -> Response:
        self.db.load(request)
        return self.fs.load(request)

    def _evict(self):
        df = self.db.get_requests()
        requests_to_evict = self.evictor.get_items_to_evict(df)
        _LOGGER.info(f"Evicting {len(requests_to_evict)} items.")
        for r in requests_to_evict:
            self.db.remove(r)
            self.fs.remove(r)
