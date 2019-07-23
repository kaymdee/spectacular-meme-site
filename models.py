
from google.appengine.ext import ndb
import time

class User(ndb.Model):
    firstName = ndb.StringProperty(required=True)
    lastName = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    friends = ndb.KeyProperty(repeated = True)
    likedPosts = ndb.KeyProperty(repeated=True)
    userPosts = ndb.KeyProperty(repeated=True)

class Post(ndb.Model):
    postTime = ndb.TimeProperty(required=True, default=time.time())
    postTitle =  ndb.StringProperty(required=True)
    postAuthor =  ndb.StringProperty(required=True)
    postContent = ndb.StringProperty(required=True)
    postDesc = ndb.StringProperty(required=True)
    #how to do image
    comments = ndb.KeyProperty(repeated=True)
    likes = ndb.IntegerProperty(required=False, default=0)

class Comment(Post):
    parentPost = ndb.KeyProperty(required=True)
