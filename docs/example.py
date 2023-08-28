import time
from pathlib import Path

import diskcache

cache = diskcache.CacheDecorator(dirpath=Path(".tmp/mycache"))
cache.store.clear()


@cache
def my_long_running_function(x):
    time.sleep(1)
    return x


if __name__ == "__main__":
    my_long_running_function(10)
    my_long_running_function(10)
    my_long_running_function(10)
    my_long_running_function(10)
    my_long_running_function(10)
