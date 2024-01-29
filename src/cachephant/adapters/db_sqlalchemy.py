import contextlib
from collections.abc import Iterator
from pathlib import Path

import pandas as pd
import sqlalchemy
from sqlalchemy.exc import NoResultFound  # type: ignore[attr-defined]
from sqlalchemy.orm import (  # type: ignore[attr-defined]
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
)

from cachephant.interfaces import (
    DatabaseInterface,
    NoRequestFoundError,
    Request,
    Response,
)


# NOTE: See https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# NOTE: This seems thread-safe, but not 100% sure, see https://stackoverflow.com/a/44123865/2135504
class Database(DatabaseInterface):
    def __init__(self, db_path: Path) -> None:
        self.engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")
        _Base.metadata.create_all(self.engine)

    def save(self, request: Request, response: Response) -> None:
        row = _RequestTable.from_request(request, response)
        with self._get_session() as s:
            s.add(row)
            s.commit()

    def load(self, request: Request) -> None:
        with self._get_session() as s:
            try:
                row = s.query(_RequestTable).filter_by(hash_str=request.hash_str).one()
            except NoResultFound as err:
                raise NoRequestFoundError from err
            else:
                row.utc_time = request.utc_time
                s.commit()

    def remove(self, request: Request) -> None:
        with self._get_session() as s:
            row = s.query(_RequestTable).filter_by(hash_str=request.hash_str).one()
            s.delete(row)
            s.commit()

    def get_requests(self, filter_dict: dict | None = None) -> pd.DataFrame:
        dct = filter_dict or {}
        with self._get_session() as s:
            query = s.query(_RequestTable).filter_by(**dct)
            return pd.read_sql(query.statement, query.session.bind)

    @contextlib.contextmanager
    def _get_session(self) -> Iterator[Session]:
        with Session(self.engine) as s:  # type: ignore[attr-defined]
            yield s


class _Base(DeclarativeBase):
    pass


class _RequestTable(_Base):
    __tablename__ = "request"

    id_: Mapped[int] = mapped_column(primary_key=True)
    hash_str: Mapped[str]
    func_name: Mapped[str]
    arg_str: Mapped[str]
    utc_time: Mapped[float]
    file_size_in_bytes: Mapped[int]

    # NOTE: Can simplify this?! See https://docs.sqlalchemy.org/en/20/orm/dataclasses.html
    @classmethod
    def from_request(cls, request: Request, response: Response) -> "_RequestTable":
        return cls(
            hash_str=request.hash_str,
            func_name=request.func_name,
            arg_str=request.arg_str,
            utc_time=request.utc_time,
            file_size_in_bytes=response.file_size_in_bytes,
        )

    def to_request(self) -> Request:
        return Request(
            hash_str=self.hash_str,
            func_name=self.func_name,
            arg_str=self.arg_str,
            utc_time=self.utc_time,
        )
