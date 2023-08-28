from pathlib import Path
from typing import Any

from diskcache.cache import Cache
from diskcache.store import AbstractStore


class FakeStore(AbstractStore):
    def get(self, id_: str) -> Any:
        del id_
        return "fake object"

    def put(self, obj: Any, id_: str) -> int:
        del obj, id_
        return 100  # bytes

    def delete(self, id_: str) -> None:
        del id_
        return

    def clear(self):
        return


def test_cache(tmp_path: Path):
    dirpath = Path(tmp_path)
    cache = Cache(dirpath, max_byte_size=250)
    cache.clear()
    cache.store = FakeStore()

    def pc():
        with cache.db.opendb() as db:
            print(db.all())

    cache.put("", "1")
    cache.put("", "2")
    cache.get("1")
    cache.put("", "3")
    pc()

    # TODO: add checks
