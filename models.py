from google.appengine.api import images
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
    postTime = ndb.DateTimeProperty(auto_now_add=True)
    postTitle =  ndb.StringProperty(required=True)
    postAuthor =  ndb.StringProperty(required=True)
    postDesc = ndb.StringProperty(required=True)
    postImage = ndb.BlobProperty(required=True)
    Comments = ndb.KeyProperty(repeated=True)
    likes = ndb.IntegerProperty(required=False, default=0)

class Comment(Post):
    comment = ndb.KeyProperty(Post, required=True)
#previously parentPost
