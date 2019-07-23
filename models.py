
from google.appengine.ext import ndb
import time
    
class Post(ndb.Model):
    postTime = ndb.TimeProperty(required=True, default=time.time())
    postTitle =  ndb.StringProperty(required=True)
    postAuthor =  ndb.StringProperty(required=True)
    postContent = ndb.StringProperty(required=True)
