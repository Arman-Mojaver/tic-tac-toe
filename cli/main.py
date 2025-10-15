import sys
from pathlib import Path

import click

sys.path.append(Path(__file__).resolve().parent.parent.as_posix())

from .seed_users import seed_users
from .utils.main import utils_subcommands


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main() -> None:
    pass


main.add_command(seed_users)
main.add_command(utils_subcommands)


if __name__ == "__main__":
    main()
