# Cachephant

![](README.assets/2024-01-25-11-21-22.png)
![](README.assets/2024-01-25-11-23-53.png)

Cachephant is a small python library which caches function output to disk and thereby avoid unnecessary recomputation. It's aimed for use in Jupyter notebooks.

## Why this library?

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

## How to use

See a minimal example in [`docs/example.py`](docs/example.py)

The cache should keep the most recently accessed items and evicts once `max_size` is exceeded.

## TODO

- [ ] Make `decorator.py` use `Cache` instead of `Store`
- [ ] Add more tests to ensure process-parallel-safe behavior
- [ ] Add CI tests
- [ ] Convert it to a proper python package and push to pypi

## Alternatives

[`joblib.Memory`](https://joblib.readthedocs.io/en/latest/auto_examples/memory_basic_usage.html) also caches the result of a function. However, I personally found two deficits:

- It does not work across jupyter notebook sessions because the cache-dir is named according to the kernel, see screenshot below (this may very well be intended, but doesn't serve my use case).
- It is unclear to me how exactly the hashing works.

```bash
cache
cache/joblib
cache/joblib/__main__--tmp-ipykernel-4032011732
cache/joblib/__main__--tmp-ipykernel-4032011732/get_gdf
cache/joblib/__main__--tmp-ipykernel-4032011732/get_gdf/4652c901c0c669e4db83383b50f91968
cache/joblib/__main__--tmp-ipykernel-4032011732/get_gdf/4652c901c0c669e4db83383b50f91968/output.pkl
cache/joblib/__main__--tmp-ipykernel-4032011732/get_gdf/4652c901c0c669e4db83383b50f91968/metadata.json
cache/joblib/__main__--tmp-ipykernel-4032011732/get_gdf/func_code.py
```

## Lessons learned

- filelock
- tinyDB
- I developed this in code-cells using VSCode

## What's the ideal caching?

- It recalculates if
  - function code changes ?!
  - function signature changes (e.g. modified kwargs, MAYBE type annotation?!)
- It does NOT recalculate if
  - jupyter kernel restarts
  - some unrelated code changes (e.g. comments, unrelated classes)
  - some called code changes (not because not desirable, just because really difficult to find out. Rather empty cache manually then)

Additional features

- ability to evict cache manually (of certain functions?)
- automatic eviction (LRU)
- Optional: specify eviction policy
- Optional: can ignore some arguments (difficult)
