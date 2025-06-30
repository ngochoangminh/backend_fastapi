import sys
import alembic.config
from loguru import logger
from dotenv import load_dotenv
from app.repositories.orm.sql_orm import *


def run(args):
    alembicArgs = ["--raiseerr", "-c", "./alembic.ini", *args]

    logger.debug(f"Calling alembic with args: {alembicArgs}")
    alembic.config.main(argv=alembicArgs)


if __name__ == "__main__":
    load_dotenv()
    argv = sys.argv
    run(argv[1:])
