
from google.appengine.ext import ndb
import time

class User(ndb.Model):
    firstName = ndb.StringProperty(required=True)
    lastName = ndb.StringProperty(required=True)
    email = ndb.StringProperty()

class Post(ndb.Model):
    postTime = ndb.TimeProperty(required=True, default=time.time())
    postTitle =  ndb.StringProperty(required=True)
    postAuthor =  ndb.StringProperty(required=True)
    postContent = ndb.StringProperty(required=True)

class Comment(Post):
    parentPost = ndb.KeyProperty(required=True)
