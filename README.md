# Cachephant

![](README.assets/2024-01-25-11-21-22.png)

Cachephant is a small python library which caches function output to disk to avoid unnecessary recomputation. It's aimed for use in Jupyter notebooks.

## Problem

There's already [`joblib.Memory`](https://joblib.readthedocs.io/en/latest/auto_examples/memory_basic_usage.html) and [`diskcache.memoize`](https://grantjenks.com/docs/diskcache/api.html#diskcache.FanoutCache.memoize). However, they didn't provide the behavior I desired (see table below):

- Joblib is very conservative and it's cache cannot be reused after restarting the Jupyter kernel. Moreover, unrelated code changes lead to cache invalidation.
- In contrast, diskcache is very liberal in its cache reuse and doesn't notice function code or signature changes. (This may be great for running a stable web app for weeks, but less idea for data science development.)

| uses cache if...            | joblib       | diskcache | cachephant                         |
| --------------------------- | ------------ | --------- | ---------------------------------- |
| Jupyter kernel restarts     | n            | y         | y                                  |
| same "resolved" arguments   | n            | n !       | y                                  |
| some unrelated code changes | n            | y         | y                                  |
| some related code changes   | n            | y         | y (n would be ideal but difficult) |
| function code changes       | n            | y !       | n                                  |
| function signature changes  | raises error | y !       | n                                  |

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
