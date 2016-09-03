from settings.config import config
from peewee import Model
from playhouse.pool import PooledMySQLDatabase

from db.mysql_model.mysql_db_init import mysql_db_init

# PooledMySQLDatabase, 连接池
db_mysql = PooledMySQLDatabase(
        config.BACKEND_MYSQL['database'],
        max_connections=config.BACKEND_MYSQL['max_connections'],
        stale_timeout=config.BACKEND_MYSQL['stale_timeout'],  # 5 minutes.
        user=config.BACKEND_MYSQL['user'],
        password=config.BACKEND_MYSQL['password'],
        host=config.BACKEND_MYSQL['host'],
        port=config.BACKEND_MYSQL['port']
)


class BaseModel(Model):
    class Meta:
        database = db_mysql

mysql_db_init(db_mysql)
