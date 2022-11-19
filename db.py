import databases
import sqlalchemy
from decouple import config

DATABASE_URL = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}" \
               f"@{config('DB_IP')}:{config('DB_PORT')}/{config('DB_NAME')}"

database = databases.Database(url=DATABASE_URL)
metadata = sqlalchemy.MetaData()
