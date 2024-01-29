# Cachephant

![](README.assets/2024-01-25-11-21-22.png)

Cachephant is a small python library which caches function output to disk to avoid unnecessary recomputation. It's aimed for use in Jupyter notebooks.

## Problem

There's already [`joblib.Memory`](https://joblib.readthedocs.io/en/latest/auto_examples/memory_basic_usage.html) and [`diskcache.memoize`](https://grantjenks.com/docs/diskcache/api.html#diskcache.FanoutCache.memoize). However, they didn't provide the behavior I desired:

| uses cache if...                                      | joblib       | diskcache | cachephant                         |
| ----------------------------------------------------- | ------------ | --------- | ---------------------------------- |
| Jupyter kernel restarts                               | n            | y         | y                                  |
| arguments leading to same "resolved" arguments change | n            | n !       | y                                  |
| some unrelated code changes                           | n            | y         | y                                  |
| some related code changes                             | n            | y         | y (n would be ideal but difficult) |
| function code changes                                 | n            | y !       | n                                  |
| function signature changes                            | raises error | y !       | n                                  |

## How to use

```python
import cachephant

cache = cachephant.get_default_cache("/path/to/dir")

@cache
def slow_function():
    time.sleep(10)
    return 3
```

You can also instantiate `cachephant.Cache()` and easily pass custom database-, file-, hash-, and evictor-classes.

## Non-goals

This library is not meant for high frequency use cases (think hundreds of cache reads/writes per second) and you'll likely see performance issues.
