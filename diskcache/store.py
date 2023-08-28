import abc
import logging
import pickle
import shutil
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


class AbstractStore(abc.ABC):
    @abc.abstractmethod
    def get(self, id_: str) -> Any:
        ...

    @abc.abstractmethod
    def put(self, obj: Any, id_: str) -> int:
        ...

    @abc.abstractmethod
    def delete(self, id_: str) -> None:
        ...

    @abc.abstractmethod
    def clear(self) -> None:
        ...


class PickleStore(AbstractStore):
    def __init__(self, dirpath: Path) -> None:
        dirpath = dirpath.absolute()
        if dirpath.exists():
            # TODO: accept non-empty dir only if has metadata matching dir?!
            LOGGER.warning(f"{dirpath=} already exists")
        else:
            dirpath.mkdir(exist_ok=True)

        self.dirpath = dirpath

    def get(self, id_: str) -> Any:
        p = self._get_path(id_)
        with p.open("rb") as f:
            return pickle.load(f)

    def put(self, obj: Any, id_: str) -> int:
        p = self._get_path(id_)
        if p.exists():
            msg = f"{id_=} already exists!"
            raise FileExistsError(msg)
        with p.open("wb") as f:
            pickle.dump(obj, f)
        return p.stat().st_size

    def delete(self, id_: str) -> None:
        p = self._get_path(id_)
        p.unlink()

    def clear(self):
        shutil.rmtree(self.dirpath)
        self.dirpath.mkdir()

    def _get_path(self, id_: str) -> Path:
        return self.dirpath / f"{id_}.pkl"
