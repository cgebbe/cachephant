from cachephant import composite
from pathlib import Path
import pytest
import logging


def test_cache(tmp_path: Path, caplog: pytest.LogCaptureFixture):
    mycache = composite.get_default_cacher(tmp_path)

    @mycache
    def myfunc(x):
        return x

    # see https://stackoverflow.com/a/59876178/2135504
    with caplog.at_level(logging.INFO):
        myfunc(3)
        assert caplog.records[-1].message == "cache miss"

        myfunc(3)
        assert caplog.records[-1].message == "cache hit"
