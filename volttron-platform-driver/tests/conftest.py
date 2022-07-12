"""Tests suite for `platform_driver_agent`."""

import json
from pathlib import Path

import pytest
from testing.volttron import TestServer as _TestServer

from platform_driver.agent import platform_driver_agent

TESTS_DIR = Path(__file__).parent
TMP_DIR = TESTS_DIR / "tmp"
FIXTURES_DIR = TESTS_DIR / "fixtures"
"""Configuration for the pytest test suite."""


@pytest.fixture()
def platform_driver():
    config_path = f"{TESTS_DIR}/cfg.json"
    config_json = {
        'driver_scrape_interval': 0.05,
        'publish_breadth_first_all': 'false',
        'publish_depth_first': 'false',
        'publish_breadth_first': 'false'
    }

    with open(config_path, 'w') as fp:
        json.dump(config_json, fp)

    yield platform_driver_agent(config_path)

    Path(config_path).unlink(missing_ok=True)


@pytest.fixture()
def volttron_test_server():
    yield _TestServer()