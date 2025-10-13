import click

from .utils.main import utils_subcommands


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main() -> None:
    pass


main.add_command(utils_subcommands)


if __name__ == "__main__":
    main()
