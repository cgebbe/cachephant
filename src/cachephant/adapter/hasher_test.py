from cachephant.adapter import hasher


def _func(x, y, o1="foo", o2=123):
    pass


def test_hasher():
    myhasher = hasher.Hasher()
    s1 = myhasher.hash(_func, 1, y=33, o2=234)
    assert isinstance(s1, str)
    print(s1)

    s2 = myhasher.hash(_func, 1, y=33)
    s3 = myhasher.hash(_func, 1, y=33, o2=123)
    assert s2 == s3


def test_resolve_args():
    a = hasher._resolve_args(_func, 1, 33, o2={"baz": 1222})
    e = {"x": 1, "y": 33, "o1": "foo", "o2": {"baz": 1222}}
    assert a == e


def test_hash_obj():
    a = hasher._hash_obj({"x": 1, "y": 33, "o1": "foo", "o2": {"foo": 1222}})
    e = "b1c3136e7ec7e5833a1babc76628be37cd49a6f62379fa47e7a912006ac8785a"
    assert a == e
