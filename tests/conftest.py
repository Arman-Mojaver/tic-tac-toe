import os

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

os.environ["ENVIRONMENT"] = "testing"

from config import config as project_config

if not project_config.is_testing():
    err = f"Invalid testing environment: {project_config}"

from src.main import app


@pytest.fixture(scope="session")
def debug(request) -> bool:
    return request.config.getoption("--d")


@pytest.fixture(scope="session", autouse=True)
def client(*, debug: bool):
    with TestClient(app) as client:
        if database_exists(project_config.SQLALCHEMY_DATABASE_URI):
            drop_database(project_config.SQLALCHEMY_DATABASE_URI)
        create_database(project_config.SQLALCHEMY_DATABASE_URI)

        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

        yield client

        if not debug:
            drop_database(project_config.SQLALCHEMY_DATABASE_URI)


@pytest.fixture
def session() -> Session:
    """Provide a SQLAlchemy session for tests."""
    engine = create_engine(project_config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine, expire_on_commit=False)  # noqa: N806
    session = Session()

    yield session

    session.close()
    engine.dispose()
