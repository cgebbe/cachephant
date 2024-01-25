from cachephant.adapter import hasher
from cachephant.interfaces import Request


def myfunc(x, y, o1="foo", o2=123):
    pass


def test_hasher():
    myhasher = hasher.Hasher()
    h1 = myhasher.hash(myfunc, 1, y=33, o2=234)
    assert h1.func_name == "myfunc"
    assert isinstance(h1.hash_str, str)

    h2 = myhasher.hash(myfunc, 1, y=33)
    h3 = myhasher.hash(myfunc, 1, y=33, o2=123)
    assert h2.hash_str == h3.hash_str


def test_resolve_args():
    a = hasher._resolve_args(myfunc, 1, 33, o2={"baz": 1222})
    e = {"x": 1, "y": 33, "o1": "foo", "o2": {"baz": 1222}}
    assert a == e


def test_hash_obj():
    a = hasher._hash_obj({"x": 1, "y": 33, "o1": "foo", "o2": {"foo": 1222}})
    e = "b1c3136e7ec7e5833a1babc76628be37cd49a6f62379fa47e7a912006ac8785a"
    assert a == e
