import time
from pathlib import Path

from assertpy import assert_that

from diskcache.decorator import CacheDecorator


def test_persistent_cache():
    logs = []
    cache = CacheDecorator(
        dirpath=Path(__file__).parent / "temp_cache",
        logfunc=logs.append,
    )
    cache.store.clear()

    @cache
    def hi(x, y=123):
        del y
        time.sleep(2)
        return x

    out = [hi(2), hi(3), hi(2, y=123)]
    assert_that(out).is_equal_to([2, 3, 2])
    assert_that(logs).is_equal_to(["cache miss", "cache miss", "cache hit"])
    cache.store.clear()
