from pathlib import Path

from cachephant.adapters import db_sqlalchemy
from cachephant.interfaces import Request, Response

_REQUEST = Request(
    func_name="myfunc",
    arg_str="irrelevant",
    utc_time=0,
    hash_str="myhash",
)
_RESPONSE = Response(
    result="myresult",
    file_size_in_bytes=0,
)


def test_db(tmp_path: Path):
    db = db_sqlalchemy.Database(tmp_path / "db.sqlite")

    db.save(_REQUEST, _RESPONSE)
    df1 = db.get_requests({"hash_str": _REQUEST.hash_str})
    assert len(df1) == 1
    assert df1.loc[0, "utc_time"] == 0

    new_time = 1
    _REQUEST.utc_time = new_time
    db.load(_REQUEST)
    df2 = db.get_requests({"hash_str": _REQUEST.hash_str})
    assert df2.loc[0, "utc_time"] == new_time

    db.remove(_REQUEST)
    df3 = db.get_requests()
    assert len(df3) == 0
