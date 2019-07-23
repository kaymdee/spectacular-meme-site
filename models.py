
from google.appengine.ext import ndb
import datetime
class BlogPost(ndb.Model):
    postTime = ndb.DateTimeProperty(required=True, default=datetime.datetime.now())
    postTitle =  ndb.StringProperty(required=True)
    postAuthor =  ndb.StringProperty(required=True)
    postContent = ndb.StringProperty(required=True)
