from cachephant import interfaces
import functools
import dataclasses
from typing import Any


@dataclasses.dataclass
class Cache:
    hasher: interfaces.HasherInterface
    fs: interfaces.FileSystemInterface
    db: interfaces.DatabaseInterface

    def __call__(self, func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            request = self.hasher.hash(func, args, kwargs)

            try:
                response = self._load(request)
            except FileNotFoundError:
                result = func(*args, **kwargs)
                response = self._save(result)

            return response.result

        return new_func

    def _save(self, request: interfaces.Request, result: Any) -> interfaces.Response:
        response = self.fs.save(request, result)
        self.db.save(request, response)
        return response

    def _load(self, request: interfaces.Request) -> interfaces.Response:
        self.db.load(request)
        return self.fs.load(request)

    def _evict(self):
        requests = self.db.get_all_requests()
        requests_to_evict = requests  # FIXME: A more complicated logic
        for r in requests_to_evict:
            self.db.remove(r)
            self.fs.remove(r)
