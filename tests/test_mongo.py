import sys,os
sys.path.append(os.path.dirname(sys.path[0]))
print(sys.path)
from backend.mongo_db.comment import CommentDB
CommentDB.add_comment('test2','good')

