from config import BACKEND_MYSQL
from peewee import Model
from playhouse.pool import PooledMySQLDatabase

#PooledMySQLDatabase
db_mysql = PooledMySQLDatabase(
    BACKEND_MYSQL['database'],
    max_connections=BACKEND_MYSQL['max_connections'],
    stale_timeout=BACKEND_MYSQL['stale_timeout'],  # 5 minutes.
    user=BACKEND_MYSQL['user'],
    password=BACKEND_MYSQL['password']
)
class BaseModel(Model):
    class Meta:
        database = db_mysql
