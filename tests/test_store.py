import tempfile
from pathlib import Path

from diskcache.store import PickleStore


def test_pickle_store():
    import geopandas as gpd
    from geopandas.testing import assert_geodataframe_equal

    dirpath = tempfile.mkdtemp()
    obj = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    hsh = "some_random_hash"
    store = PickleStore(Path(dirpath))

    store.put(obj, hsh)
    reloaded = store.get(hsh)
    assert_geodataframe_equal(obj, reloaded)

    store.clear()  # to remove the tempdir, not strictly necessary
