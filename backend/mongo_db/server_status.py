import config
from backend.mongo_db import DB_mongo
import functools

class ServerStatus():
    '''
    url访问记录
    '''
    _collection=DB_mongo['serverstatus']
    @classmethod
    def visitor_url_up(cls,url):
        url_status=cls._collection.find_one({'url':url})
        if url_status:
            cls._collection.update({'url':url},{'$inc':{'count':1}})
            return url_status['count']+1
        else:
            cls._collection.save({'url':url,'count':0})
            return 0


def url_count(request):
    @functools.wraps(request)
    def _func(handler,*args, **kwargs):
        setattr(handler,'url_count',ServerStatus.visitor_url_up(handler.request.path))
        return_val = request(handler, *args, **kwargs)
        return return_val
    return _func