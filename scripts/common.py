import json
import os
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
USER_AGENT = "portfolio-sync (https://danielcorralesalonso.github.io)"


def get_json(url, headers=None):
    """GET a JSON document. Returns None on 404, raises on any other error."""
    request = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": USER_AGENT, **(headers or {})}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def github_headers():
    token = os.environ.get("GITHUB_TOKEN")
    return {"Authorization": f"Bearer {token}"} if token else {}


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path, items, header):
    with open(path, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(items, f, allow_unicode=True, sort_keys=False, width=1000)
