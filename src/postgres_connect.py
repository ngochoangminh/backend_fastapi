import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

class PostgresSetting():

    POSTGRES_HOST : str = os.getenv("POSTGRES_HOST")
    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASS : str = os.getenv("POSTGRES_PASS")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB : str = os.getenv("POSTGRES_DB")

    POSTGRES_URL : str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

if __name__ == '__main__':
    postgres_engine = create_engine(PostgresSetting.POSTGRES_URL)
    