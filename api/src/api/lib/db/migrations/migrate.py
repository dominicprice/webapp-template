import sys
from datetime import datetime
from time import monotonic
from typing import Any

from api.lib.db.migrations.migration import (
    BaseMigration,
    PythonMigration,
    SqlMigration,
)
from sqlalchemy import Engine, inspect, text

migrations: list[BaseMigration] = [
    SqlMigration("m001_init.sql"),
]

migrations_table_schema = """
CREATE TABLE Migrations (
  name TEXT NOT NULL PRIMARY KEY,
  hash TEXT NOT NULL,
  applied_at DATETIME NOT NULL
)
"""


def migrate(db: Engine, verbose: bool = True):
    def log(*args: Any):
        if verbose:
            print(*args, file=sys.stderr)

    log("Applying migrations...")

    with db.begin() as conn:
        i = inspect(conn)
        if not i.has_table("Migrations"):
            if verbose:
                log("Migrations table does not exist, creating now...")
            conn.execute(text(migrations_table_schema))

        n_applied = 0
        start = monotonic()
        for migration in migrations:
            # check if migration has been previously applied
            res = conn.execute(
                text("SELECT hash FROM Migrations WHERE name = :name"),
                {"name": migration.name()},
            ).one_or_none()

            if res is None:
                # apply migration
                migration.apply(conn)
                conn.execute(
                    text(
                        "INSERT INTO Migrations (name, hash, applied_at) VALUES (:name, :hash, :applied_at)"
                    ),
                    {
                        "name": migration.name(),
                        "hash": migration.hash(),
                        "applied_at": datetime.now().isoformat(),
                    },
                )
                n_applied += 1
            else:
                # check integrity of migration
                if res[0] != migration.hash():
                    log(
                        "migration",
                        migration.name(),
                        "has different hash to previously applied value",
                    )
        stop = monotonic()

        log(f"Applied {n_applied} migrations in {stop - start}s")
