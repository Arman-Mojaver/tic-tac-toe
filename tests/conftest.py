import os

import pytest
from fastapi.testclient import TestClient

from src.main import app

os.environ["ENVIRONMENT"] = "testing"

from config import config as project_config

if not project_config.is_testing():
    err = f"Invalid testing environment: {project_config}"


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
