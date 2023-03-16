import pytest

from .network import setup_visca, setup_geth


@pytest.fixture(scope="session")
def visca(tmp_path_factory):
    path = tmp_path_factory.mktemp("visca")
    yield from setup_visca(path, 26650)


@pytest.fixture(scope="session")
def geth(tmp_path_factory):
    path = tmp_path_factory.mktemp("geth")
    yield from setup_geth(path, 8545)


@pytest.fixture(
    scope="session", params=["visca", "visca-ws"]
)
def visca_rpc_ws(request, visca):
    """
    run on both visca and visca websocket
    """
    provider = request.param
    if provider == "visca":
        yield visca
    elif provider == "visca-ws":
        visca_ws = visca.copy()
        visca_ws.use_websocket()
        yield visca_ws
    else:
        raise NotImplementedError
