import functools
from pathlib import Path

import filelock

from diskcache.store import PickleStore
from diskcache.utils import hash_obj, resolve_args


class CacheDecorator:
    def __init__(self, dirpath: Path, logfunc=print) -> None:
        self.dirpath = dirpath
        self.store = PickleStore(dirpath)
        self.logfunc = logfunc

    def __call__(self, func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            resolved_args = resolve_args(func, *args, **kwargs)
            hash_str = hash_obj(resolved_args)

            # Use a filelock to prevent two parallel processes
            # working on the same hash value.
            # TODO: Use the _get_lock function from Cache
            with filelock.SoftFileLock(self.dirpath / f"{hash_str}.lock"):
                try:
                    out = self.store.get(hash_str)
                    self.logfunc("cache hit")
                except FileNotFoundError:
                    self.logfunc("cache miss")
                    out = func(*args, **kwargs)
                    self.store.put(out, hash_str)
            return out

        return new_func
