import sys
sys.path.append('./')
print(sys.path)
from backend.mongo_db.comment import CommentDB
CommentDB.add_comment('test2','good')

