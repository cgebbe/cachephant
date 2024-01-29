import pytest

from cachephant.adapters.evictor import LeastRecentlyUsedEvictor
from cachephant.interfaces import Request


@pytest.mark.parametrize(
    ("max_count", "expected_idxs"),
    [
        (2, [0, 2]),
        (0, []),
    ],
)
def test_evictor(max_count, expected_idxs):
    lst = [
        Request("hash", "func", "args", 0),
        Request("hash", "func", "args", 10),
        Request("hash", "func", "args", 2),
        Request("hash", "func", "args", 20),
    ]
    df = Request.create_pandas_df(lst)
    evictor = LeastRecentlyUsedEvictor(max_count=max_count)

    items = evictor.get_items_to_evict(df)

    assert items == [lst[i] for i in expected_idxs]
