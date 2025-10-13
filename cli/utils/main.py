import click

from .info import get_info


@click.group(name="utils", help="Utils")
def utils_subcommands() -> None:
    pass


utils_subcommands.add_command(get_info)
