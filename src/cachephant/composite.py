from cachephant import cache
from cachephant.adapters import db_sqlalchemy, filesystem, hasher
from pathlib import Path


def get_default_cacher(cache_dirpath: Path) -> cache.Cache:
    return cache.Cache(
        hasher=hasher.Hasher(),
        db=db_sqlalchemy.Database(db_path=cache_dirpath / "db.sqlite"),
        fs=filesystem.FileSystem(cache_dirpath),
    )
