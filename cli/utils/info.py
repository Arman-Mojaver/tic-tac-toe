import pathlib
import sys

import click


def count_lines_of_code(path: pathlib.Path) -> int:
    exclude_dirs = {
        ".venv",
        "venv",
        "__pycache__",
        "build",
        "dist",
        ".git",
        ".mypy_cache",
    }
    total_lines = 0

    for py_file in path.rglob("*.py"):
        if any(excluded in py_file.parts for excluded in exclude_dirs):
            continue

        try:
            content = py_file.read_text(encoding="utf-8")
            total_lines += len(content.splitlines())
        except (UnicodeDecodeError, OSError) as e:
            err = f"Skipping {py_file}: {e}"
            click.echo(err)


    return total_lines


def get_project_size(path: pathlib.Path) -> str:
    total_bytes = 0

    for f in path.rglob("*"):
        if f.is_file():
            total_bytes += f.stat().st_size

    size_gb = total_bytes / (1024 ** 3)
    return f"{size_gb:.3f} GB"


@click.command("info", help="Get project information")
def get_info() -> None:
    project_root = pathlib.Path.cwd()

    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    total_lines = count_lines_of_code(project_root)
    size = get_project_size(project_root)

    click.echo("\nProject Info")
    click.echo("------------")
    click.echo(f"Root: {project_root}")
    click.echo(f"Python version: {python_version}")
    click.echo(f"Total lines of Python code: {total_lines}")
    click.echo(f"Size on disk: {size}")
