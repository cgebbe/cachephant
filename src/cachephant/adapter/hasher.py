from typing import Any, Callable
from cachephant import interfaces
from cachephant.interfaces import Request
import inspect
import deepdiff


class Hasher(interfaces.HasherInterface):
    def hash(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Request:
        resolved_args = _resolve_args(func, *args, **kwargs)
        return _hash_obj(
            {
                "source_code": inspect.getsource(func),
                "resolved_args": resolved_args,
            }
        )


def _resolve_args(func, *args, **kwargs):
    sig = inspect.signature(func)
    bounds = sig.bind(*args, **kwargs)
    bounds.apply_defaults()
    return bounds.arguments


def _hash_obj(obj: Any):
    """Hashes arbitrary objects using deepdiff.DeepHash.

    Note: This is surprisingly difficult, see
    - https://stackoverflow.com/questions/5884066/hashing-a-dictionary
    - https://hynek.me/articles/hashes-and-equality/

    Just hoping that DeepHash is somewhat sensible!
    """
    return deepdiff.DeepHash(obj)[obj]
