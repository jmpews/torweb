from backend.redis_db import DB_redis

class RateLimit():
    _db=DB_redis
    _key='ratelimit:'
    @classmethod
    def ratelimit(cls,ip):
        key=cls._key+ip
        if cls._db.exists(key):
            t=cls._db.incr(key)
            if t>7:
                return cls._db.ttl(key)
        else:
            p = cls._db.pipeline()
            p.incr(key)
            p.expire(key,5)
            p.execute()
        return False



