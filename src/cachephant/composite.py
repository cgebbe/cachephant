from pathlib import Path

from cachephant import cache
from cachephant.adapters import db_sqlalchemy, filesystem, hasher


def get_default_cache(cache_dirpath: Path) -> cache.Cache:
    return cache.Cache(
        hasher=hasher.Hasher(),
        db=db_sqlalchemy.Database(db_path=cache_dirpath / "db.sqlite"),
        fs=filesystem.FileSystem(str(cache_dirpath)),
    )
