import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


_initial_activities = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(_initial_activities)
    yield


@pytest.fixture
def app():
    return app_module.app


@pytest.fixture
def client(app):
    return TestClient(app)
