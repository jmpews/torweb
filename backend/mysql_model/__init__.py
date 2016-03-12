import config
from peewee import Model
from playhouse.db_url import connect
from playhouse.pool import PooledMySQLDatabase
db_mysql = connect(config.BACKEND_MYSQL)

# PooledMySQLDatabase
#db = PooledMySQLDatabase(
#    'seebugticket',
#    max_connections=32,
#    stale_timeout=300,  # 5 minutes.
#    user='root',
#    password='root'
#)
class BaseModel(Model):
    class Meta:
        database = db_mysql
