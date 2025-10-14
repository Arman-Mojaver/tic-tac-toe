from __future__ import annotations

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

from database.models import Match, Move, User
from src.main import app


@pytest.fixture(scope="session")
def debug(request) -> bool:
    return request.config.getoption("--d")


@pytest.fixture(scope="session", autouse=True)
def client():
    with TestClient(app) as client:
        if database_exists(project_config.SQLALCHEMY_DATABASE_URI):
            drop_database(project_config.SQLALCHEMY_DATABASE_URI)
        create_database(project_config.SQLALCHEMY_DATABASE_URI)

        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

        yield client


@pytest.fixture
def session() -> Session:
    """Provide a SQLAlchemy session for tests."""
    engine = create_engine(project_config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine, expire_on_commit=False)  # noqa: N806
    session = Session()

    yield session

    session.close()
    engine.dispose()


@pytest.fixture
def fake_id():
    return 12345678


@pytest.fixture
def create_user(session):
    def _create_user(name="TestUser", password="secret"):  # noqa: S107
        user = User(name=name, password=password)
        session.add(user)
        session.commit()
        return user

    return _create_user


@pytest.fixture
def create_match(session, create_user):
    user_1 = create_user(name="PlayerX", password="secret")
    user_2 = create_user(name="PlayerO", password="secret")

    def _create_match(
        user_x: User | None = None,
        user_o: User | None = None,
        winner: User | None = None,
    ):
        if not user_x:
            user_x = user_1

        if not user_o:
            user_o = user_2

        match = Match(user_x_id=user_x.id, user_o_id=user_o.id, winner=winner)
        session.add(match)
        session.commit()
        session.refresh(match)
        return match

    return _create_match


@pytest.fixture
def create_move(session, create_match):
    def _create_move(match: Match, user: User, x: int = 0, y: int = 1, order: int = 1):
        move = Move(
            match_id=match.id,
            user_id=user.id,
            coordinate_x=x,
            coordinate_y=y,
            move_order=order,
        )
        session.add(move)
        session.commit()
        session.refresh(move)
        return move

    return _create_move
