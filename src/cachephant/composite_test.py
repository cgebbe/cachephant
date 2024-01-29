import logging
from pathlib import Path

import pytest

from cachephant import composite


def test_cache(tmp_path: Path, caplog: pytest.LogCaptureFixture):
    mycache = composite.get_default_cache(tmp_path)

    @mycache
    def myfunc(x):
        return x

    # see https://stackoverflow.com/a/59876178/2135504
    with caplog.at_level(logging.INFO):
        myfunc(3)
        assert caplog.records[0].message == "cache miss"
        assert caplog.records[1].message == "Evicting 0 items."

        myfunc(3)
        assert caplog.records[2].message == "cache hit"
