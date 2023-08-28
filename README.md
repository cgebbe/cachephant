# disk_cacher

This is a small library which can cache function output and thereby avoid unnecessary recomputation. It's not yet completely finished

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
