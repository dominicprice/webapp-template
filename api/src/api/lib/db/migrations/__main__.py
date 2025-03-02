import click
from api.lib.db.sql import engine
from api.lib.db.migrations.migrate import migrate


@click.command("migrate")
@click.option("-v", "--verbose", is_flag=True)
def main(verbose: bool):
    migrate(engine, verbose=verbose)


if __name__ == "__main__":
    main()
