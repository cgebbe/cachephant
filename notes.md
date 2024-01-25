# Notes during implementation

## API new go

- Hasher.hash()

  - if not hash exists...
    - result = ...
    - cache.put(hash_data)
  - cache.load(hash_data)

- during cache.put
  - cache.evict()
  - ... ?

## User story

run uncached request

- `hasher.hash(func) -> Request`
- `cache.load(request)` -> fails
- run function -> `result`
- `cache.save(item)`
  - save result in file `fs.save(request, result)`
  - add DB entry `db.save(request, result)` (request.rel_path)
- return `Result`

run cached request and evict

- `hash` request
- return `cache.load(request)`
  - `db.load(request)` # to update last used date
  - `fs.load(request)`

eviction (not sure yet WHEN to run)

- `cache.evict(func_name=..., max_count=...)`
  - check `db.get_all_requests()`
  - for request to evict...
    - `db.remove(request)`
    - `fs.remove(request)`

when to run eviction?

- before `cache.put` <-- maybe safest for now although not performant?
- after `cache.put`
- as background process

## Alternatives

- https://stackoverflow.com/questions/16463582/memoize-to-disk-python-persistent-memoization
- https://stackoverflow.com/questions/17999204/lru-cache-on-hard-drive-python

## APIs

Metadata

- Cache = Store + Metadata
  - get(hsh)
    - return Store.get(hsh)
  - put(hsh, item)
    - store.put(..)
    - MetadataStore.put(hsh, info_dict)
    - MetadataStore.get_evicted_items
- Store
  - get(hsh)
  - put(obj, hsh) -> byte_size?!
- Hasher
  - function kwargs + id
  - https://stackoverflow.com/questions/830937/python-convert-args-to-kwargs
- CacheItem
  - hash = ...
- MetadataStorage
  - add(item)

## TODOs

- make a few proper test cases for the Cache (in particular with parallel processing!)
- use logging statements instead of logfunc (and maybe with different levels of verbosity?!)

## MetadataStorage

- How to store metadata?
  - id
  - byte_size
  - last_accessed
  - last_modified
  - ...

Implementation options:

- sqlite3
  - is it thread-safe? does it need a lock?
  - https://stackoverflow.com/a/2894830/2135504
  - https://stackoverflow.com/a/6969938/2135504
- sqlite dict
  - https://github.com/RaRe-Technologies/sqlitedict
  - hmm... more of a key-value store than RDBM
- pandas and sqlite?
  - https://datacarpentry.org/python-ecology-lesson/09-working-with-sql/index.html
  - https://stackoverflow.com/a/36029761/2135504
  - ensure closing DB
  - https://codereview.stackexchange.com/a/182706/202014
  - ah, might actually work because can select columns!
  - maybe not as great, because we don`t fix schema?! Also not as flexible (e.g. select only last accessed! or modify only one thing...)
- tinydb
  - https://github.com/msiemens/tinydb (4.7k stars)
  - nice, but rather for document management
- sqlalchemy and sqlite is likely the solution
  - https://docs.sqlalchemy.org/en/20/orm/quickstart.html
  - A bit more tricky, but seems like correct choice

## Why is joblib not sufficient?

- does not work across jupyter notebook sessions because dir is named according to kernel (this may very well be intended, but doesn't serve my use case)
- unclear to me how exactly hashing works

```
cache
cache/joblib
cache/joblib/__main__--tmp-ipykernel-4032011732
cache/joblib/__main__--tmp-ipykernel-4032011732/get_gdf
cache/joblib/__main__--tmp-ipykernel-4032011732/get_gdf/4652c901c0c669e4db83383b50f91968
cache/joblib/__main__--tmp-ipykernel-4032011732/get_gdf/4652c901c0c669e4db83383b50f91968/output.pkl
cache/joblib/__main__--tmp-ipykernel-4032011732/get_gdf/4652c901c0c669e4db83383b50f91968/metadata.json
cache/joblib/__main__--tmp-ipykernel-4032011732/get_gdf/func_code.py
```

## TODO

- also hash function code and at least warn when changed? Not sure...
