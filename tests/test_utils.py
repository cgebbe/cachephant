import time
from pathlib import Path

from diskcache.utils import SafeTinyDB, hash_obj, resolve_args


def test_resolve_args():
    def func(x, y, o1="foo", o2=123):
        pass

    a = resolve_args(func, 1, 33, o2={"foo": 1222})
    e = {"x": 1, "y": 33, "o1": "foo", "o2": {"foo": 1222}}
    assert a == e


def test_hash_obj():
    a = hash_obj({"x": 1, "y": 33, "o1": "foo", "o2": {"foo": 1222}})
    e = "b1c3136e7ec7e5833a1babc76628be37cd49a6f62379fa47e7a912006ac8785a"
    assert a == e


def read(x):
    db_filepath = Path(".tmp/db.json")
    db_filepath.parent.mkdir(exist_ok=True, parents=True)
    database = SafeTinyDB(db_filepath)

    with database.opendb() as db:
        print("entering")
        db.all()  # verify no error
        time.sleep(1)
        print("exiting")


def test_parallel_db_access_succeeds():
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(3) as exec:
        future = exec.map(read, range(4))
        list(future)
