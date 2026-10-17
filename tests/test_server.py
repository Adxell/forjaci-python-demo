import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from app.server import Handler, greet


def test_greet():
    assert greet("ada") == "hello, ada"
    assert greet("  ") == "hello, world"


@pytest.fixture
def base_url():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


def get(url):
    with urllib.request.urlopen(url) as resp:
        return resp.status, json.loads(resp.read())


def test_root(base_url):
    status, body = get(base_url + "/?name=forjaci")
    assert status == 200
    assert body["message"] == "hello, forjaci"


def test_healthz(base_url):
    assert get(base_url + "/healthz") == (200, {"status": "ok"})


def test_not_found(base_url):
    with pytest.raises(urllib.error.HTTPError) as err:
        get(base_url + "/missing")
    assert err.value.code == 404
