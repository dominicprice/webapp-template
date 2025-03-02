import abc
import importlib.util
import random
import string
from hashlib import sha256
from pathlib import Path

import sqlparse
from sqlalchemy import Connection, text

schema_dir = Path(__file__).parent / "schema"


class BaseMigration(abc.ABC):
    def apply(self, conn: Connection): ...
    def hash(self) -> str: ...
    def name(self) -> str: ...


class SqlMigration(BaseMigration):
    def __init__(self, filename: str):
        self.filename = filename

    def apply(self, conn):
        with open(schema_dir / self.filename) as f:
            script = f.read()
        statements = sqlparse.split(script)
        for stmt in statements:
            conn.execute(text(stmt))

    def hash(self):
        with open(schema_dir / self.filename, "rb") as f:
            return sha256(f.read()).hexdigest()

    def name(self):
        return self.filename


class PythonMigration(BaseMigration):
    def __init__(self, filename: str):
        self.filename = filename

    def apply(self, conn):
        n = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
        spec = importlib.util.spec_from_file_location(n, schema_dir / self.filename)
        if spec is None:
            raise RuntimeError(f"spec is None for {self.filename}")
        loader = spec.loader
        if loader is None:
            raise RuntimeError(f"spec.loader is None for {self.filename}")
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        module.apply(conn)

    def hash(self):
        with open(schema_dir / self.filename, "rb") as f:
            return sha256(f.read()).hexdigest()

    def name(self):
        return self.filename
