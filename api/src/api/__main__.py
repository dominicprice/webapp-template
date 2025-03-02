import click
import uvicorn
from api.lib.config import DEBUG, SERVER_HOST, SERVER_PORT
from api.lib.db.migrations.migrate import migrate
from api.lib.db.sql import engine


@click.command("api")
def main():
    # run database migrations
    migrate(engine)

    # run server
    uvicorn.run(
        "api.server:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=DEBUG,
    )


if __name__ == "__main__":
    main()
