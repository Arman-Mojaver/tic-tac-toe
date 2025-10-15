import click

from database import session
from database.models import User

USERS = [
    User(name="Alice", password="password1"),  # noqa: S106
    User(name="Bob", password="password2"),  # noqa: S106
    User(name="Charlie", password="password3"),  # noqa: S106
    User(name="Diana", password="password4"),  # noqa: S106
    User(name="Eve", password="password5"),  # noqa: S106
]


@click.command("seed", help="Seed database with users")
def seed_users() -> None:
    try:
        session.add_all(USERS)
        session.commit()
        click.echo("✅ Seeded 5 users successfully.")
    except Exception as e:  # noqa: BLE001
        session.rollback()
        click.echo(f"❌ Failed to seed users: {e}")
    finally:
        session.close()
