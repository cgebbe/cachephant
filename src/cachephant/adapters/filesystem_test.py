from cachephant.adapters import filesystem
from cachephant.interfaces import Request
from pathlib import Path

_REQUEST = Request(
    func_name="myfunc",
    arg_str="irrelevant",
    utc_time=0,
    hash_str="myhash",
)
_RESULT = _REQUEST  # just use some custom class for pickling


def test_fs(tmp_path: Path):
    fs = filesystem.FileSystem(
        prefix=str(tmp_path),
        protocol="file",
    )

    response = fs.save(_REQUEST, _RESULT)
    reloaded = fs.load(_REQUEST)
    assert response == reloaded

    fs.remove(_REQUEST)
    files = [x for x in tmp_path.glob("*") if x.is_file()]
    assert not files
