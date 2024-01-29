from collections.abc import Iterable

import pandas as pd

from cachephant.interfaces import EvictorInterface, Request


class LeastRecentlyUsedEvictor(EvictorInterface):
    def __init__(self, max_count: int) -> None:
        super().__init__()
        self.max_count = max_count

    def get_items_to_evict(self, df: pd.DataFrame) -> Iterable[Request]:
        df = df.sort_values(by=Request.fields().utc_time, ascending=True)
        return (
            df.iloc[: -self.max_count, :]
            .apply(lambda row: Request.from_row(row), axis=1, result_type="reduce")
            .to_list()
        )
