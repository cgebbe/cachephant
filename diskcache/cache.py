import logging
import time
from contextlib import contextmanager
from pathlib import Path

import filelock
import pandas as pd
from tinydb import Query

from diskcache.store import AbstractStore, PickleStore
from diskcache.utils import SafeTinyDB

LOGGER = logging.getLogger(__name__)


class Cache:
    def __init__(
        self,
        dirpath: Path,
        max_byte_size: int = 0,
        max_item_count: int = 0,
    ) -> None:
        self.dirpath = dirpath
        self.store: AbstractStore = PickleStore(dirpath)
        self.db = SafeTinyDB(self.db_path)

        self.max_byte_size = max_byte_size
        self.max_item_count = max_item_count

    @property
    def db_path(self) -> Path:
        return self.dirpath / "db.json"

    def put(self, obj, id_: str):
        byte_size = self.store.put(obj, id_)
        info = {
            "id_": id_,
            "byte_size": byte_size,
            "last_accessed_time": time.time_ns(),
            "created_time": time.time_ns(),
        }
        with self.db.opendb() as db:
            db.insert(info)
        self._evict_objects()

    def get(self, id_):
        obj = self.store.get(id_)
        query = Query()
        with self.db.opendb() as db:
            LOGGER.info(f"Udpating {id_}")
            db.update(
                {"last_accessed_time": time.time_ns()},
                query.id_ == id_,
            )
        return obj

    def clear(self):
        self.store.clear()
        self.db_path.unlink(missing_ok=True)

    def _evict_objects(self):
        with self.db.opendb() as db:
            df = pd.DataFrame(db.all())
        # earliest time should be top
        df = df.sort_values(by="last_accessed_time", ascending=True)

        delete_list = []
        while self._requires_eviction(df):
            delete_list.append(df.loc[df.index[0], "id_"])
            df = df.iloc[1:]

        for id_ in delete_list:
            LOGGER.info(f"deleting {id_}")
            # Prevent deleting an object, which another process is currently reading.
            with self._get_lock(id_):
                self.store.delete(id_)

                query = Query()
                with self.db.opendb() as db:
                    db.remove(query.id_ == id_)

    def _requires_eviction(self, df: pd.DataFrame) -> bool:
        if self.max_byte_size and df["byte_size"].sum() > self.max_byte_size:
            return True
        if self.max_item_count and len(df) > self.max_item_count:
            return True
        return False

    @contextmanager
    def _get_lock(self, id_):
        with filelock.SoftFileLock(self.dirpath / f"{id_}.lock"):
            yield
