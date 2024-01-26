from cachephant.interfaces import (
    DatabaseInterface,
    Request,
    Response,
    NoRequestFoundError,
)
from typing import Optional
import pandas as pd
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Session
from sqlalchemy.exc import NoResultFound
import sqlalchemy
from pathlib import Path


# NOTE: See https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# NOTE: This seems thread-safe, but not 100% sure, see https://stackoverflow.com/a/44123865/2135504
class Database(DatabaseInterface):
    def __init__(self, db_path: Path) -> None:
        self.engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")
        _Base.metadata.create_all(self.engine)

    def save(self, request: Request, response: Response) -> None:
        row = _RequestTable.from_request(request, response)
        with Session(self.engine) as s:
            s.add(row)
            s.commit()

    def load(self, request: Request) -> None:
        with Session(self.engine) as s:
            try:
                row = s.query(_RequestTable).filter_by(hash_str=request.hash_str).one()
            except NoResultFound as err:
                raise NoRequestFoundError from err
            else:
                row.utc_time = request.utc_time
                s.commit()

    def remove(self, request: Request) -> None:
        with Session(self.engine) as s:
            row = s.query(_RequestTable).filter_by(hash_str=request.hash_str).one()
            s.delete(row)
            s.commit()

    def get_requests(self, filter_dict: Optional[dict] = None) -> pd.DataFrame:
        dct = filter_dict or {}
        with Session(self.engine) as s:
            query = s.query(_RequestTable).filter_by(**dct)
            return pd.read_sql(query.statement, query.session.bind)


class _Base(DeclarativeBase):
    pass


class _RequestTable(_Base):
    __tablename__ = "request"

    id: Mapped[int] = mapped_column(primary_key=True)
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
