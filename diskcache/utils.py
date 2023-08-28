import inspect
from contextlib import contextmanager
from pathlib import Path

import filelock
from deepdiff import DeepHash
from tinydb import TinyDB, middlewares, storages


def resolve_args(func, *args, **kwargs):
    sig = inspect.signature(func)
    bounds = sig.bind(*args, **kwargs)
    bounds.apply_defaults()
    return bounds.arguments


def hash_obj(obj):
    """Hashes arbitrary objects using deepdiff.DeepHash.

    Note: This is surprisingly difficult, see
    - https://stackoverflow.com/questions/5884066/hashing-a-dictionary
    - https://hynek.me/articles/hashes-and-equality/

    Just hoping that DeepHash is somewhat sensible!
    """
    return DeepHash(obj)[obj]


class SafeTinyDB:
    """TinyDB with caching and filelocking (for safe parallel processing)."""

    def __init__(self, path) -> None:
        self.db = TinyDB(
            path,
            storage=middlewares.CachingMiddleware(storages.JSONStorage),
        )
        self.lock = filelock.SoftFileLock(Path(path).with_suffix(".lock"))

    @contextmanager
    def opendb(self) -> TinyDB:
        with self.lock, self.db as db:
            yield db
