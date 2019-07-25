#main.py
# the import section
import webapp2
import jinja2
import os
import time
import models
from datetime import datetime

from google.appengine.api import images
import google.appengine
from google.appengine.api import users
from google.appengine.ext import ndb
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#will redirect to GLogin if the user is not logged into Google
#will redirect to create new profile if the user is logged into google but not register with our Website
#Logic tree:
#User G Logged and registered: returns signInOrProfileHtml and signoutHtml a dictionary
#User G Logged and not reged: redirect to CreateNewProfileHandler
#User not G Logged or reg: redirect to G Log -> CreateNewProfileHandler
#User not GLogged but reged: redirect to GLog -> main page
class Image(webapp2.RequestHandler):
    def get(self):
        post_key = ndb.Key(urlsafe=self.request.get('img_id'))
        post = post_key.get()
        if post.postImage:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(post.postImage)
        else:
            self.response.out.write('No image')
def authUser():
    gUser = users.get_current_user()
    #If user is G logged in
    if gUser:
        user = models.User.get_by_id(gUser.user_id())

        #user object exists already in data base
        if user:
            signoutHtml = jinja2.Markup('<a href="%s">Sign out</a>' % (
                users.create_logout_url('/')))
            signInOrProfileHtml = jinja2.Markup('<a id="profile.html" href="profile.html">Profile</a>')
            return {"signInOrProfileHtml":signInOrProfileHtml,
                    "signoutHtml":signoutHtml}
        #User has not been to our site
        else:
            return webapp2.redirect("/createNewProfile.html")
    else: #user isnt logged in and we need to log them in
        return webapp2.redirect((users.create_login_url('/createNewProfile.html')))

#returns the account HTML tags as a dictionary {"signInProfile" : accordinghtml, }

def getAccountHtml():
    gUser = users.get_current_user()
    #If user google is logged in
    if gUser:
        emailAddress = gUser.nickname()
        user = models.User.get_by_id(gUser.user_id())
        signoutHtml = jinja2.Markup('<a href="%s">Sign out</a>' % (
            users.create_logout_url('/')))
        #user object exists already in data base
        if user:
            signInOrProfileHtml = jinja2.Markup('<a id="profile.html" href="profile.html">Profile</a>')
        #User has not been to our site
        else:
            signInOrProfileHtml = jinja2.Markup('<a id="createNewProfile.html" href="createNewProfile.html">Sign Up</a>')
    else: #user isnt logged in and we need to log them in
        signoutHtml = ""
        signInOrProfileHtml = jinja2.Markup('<a href="%s">Sign In with Google</a>' % (users.create_login_url('/createNewProfile.html')))
    return {"signInOrProfileHtml" : signInOrProfileHtml, "signoutHtml": signoutHtml}
#this is a wip.
# the handler section
class MainPage(webapp2.RequestHandler):
    def get(self):

        post_entity_list = models.Post.query().order(models.Post.postTime).fetch()


        self.response.headers['Content-Type'] = 'html' #change this to write html!
        template = jinja_env.get_template('templates/index.html')
        dict = {
            "memePosts": post_entity_list,
        }
        dict.update(getAccountHtml())

        self.response.write(template.render(dict))

    def post(self):
        post_key = ndb.Key(urlsafe=self.request.get('post_id'))
        post = post_key.get()
        post.likes += 1
        post.put()
        self.get()

class CreateNewProfileHandler(webapp2.RequestHandler):
    def get(self):
        if not isinstance(authUser(),webapp2.Response):
            return webapp2.redirect("/index.html")#shouldn't be here if profile already exists

        template = jinja_env.get_template('templates/createNewProfile.html')
        self.response.write(template.render())
    def post(self):
        # print "post running"
        #create new user from the form
        gUser = users.get_current_user()
        if not gUser:
            # print "kicked out"
            return webapp2.redirect("index.html")
        firstName = self.request.get("firstName")
        lastName = self.request.get("lastName")
        user = models.User(email = gUser.email(),firstName=firstName, lastName=lastName, id=gUser.user_id())
        user.put()
        return webapp2.redirect("/index.html")

class FroggerPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        story_template = jinja_env.get_template('templates/frogger.html')
        self.response.write(story_template.render())

class NewPostPage(webapp2.RequestHandler):
    def get(self): #for a get request
        authResp = authUser()
        if(isinstance(authResp,webapp2.Response)):
            return authResp#stop code execution if the user has been directed

        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        template = jinja_env.get_template('templates/newPost.html')
        self.response.write(template.render())

class ShowPostPage(webapp2.RequestHandler):
    def get(self):
        pass

    def post(self):
        Title = self.request.get("post-title")
        Author = self.request.get("post-author")
        Description = self.request.get("post-description")
        Image = self.request.get("post-image")

        post = models.Post(postTitle = Title, postAuthor = Author, postDesc = Description, postImage = Image)
        post.put()

        temp_dict = {"postTitle": Title,
                    "postAuthor": Author,
                    "postDesc": Description,
                    "postDate": "now",
                    "postImage": jinja2.Markup('<img id = "size" src="/img?img_id=%s"></img>' %
                        post.key.urlsafe())
                }

        template = jinja_env.get_template("templates/showPost.html")




        self.response.write(template.render(temp_dict))

    # postDict = {#DASHES IN JINJA ARE FOR WHITESPACE CONTROL. NOT ALLOWED FOR JINJA VARIABLES
    #         "postTitle" : Title,
    #         "postAuthor" : Author,
    #         "postContent" : Description,
    #         # "postDate" : .new_post_entity.get(postTime),
    #     }
    #     self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        # template = jinja_env.get_template('templates/showPost.html')
        # self.response.write(template.render(postDict))

class ViewPostsPage(webapp2.RequestHandler):
    def get(self):
        blogPosts = models.Post.query().order(models.BlogPost.postTime).fetch()
        template = jinja_env.get_template("templates/viewPosts.html")
        self.response.write(template.render({"blogPosts":blogPosts}))

class ViewProfileHandler(webapp2.RequestHandler):
    def get(self):
        authResp = authUser()
        if(isinstance(authResp,webapp2.Response)):
            return authResp#stop code execution if the user has been directed

        gUser = users.get_current_user()
        user = models.User.get_by_id(gUser.user_id())
        template = jinja_env.get_template("templates/profile.html")
        dict = {"firstName" : user.firstName,
                "lastName" : user.lastName,
                "email" : user.email,
                }
        dict.update(authResp)#add on the html for the account tags

        self.response.write(template.render(dict))
        #why this dict?
class PageNotFoundHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        no_page_template = jinja_env.get_template("templates/pagenotfound.html")
        self.response.write(no_page_template.render())
# the app configuration section
app = webapp2.WSGIApplication([
    ("/", MainPage),
    ('/index.*', MainPage), #this maps the root url to the Main Page Handler
    ('/frogger.*', FroggerPage),
    ("/newPost.*", NewPostPage),
    ("/showPost.*", ShowPostPage),
    ("/viewPosts.*", ViewPostsPage),
    ("/createNewProfile.*", CreateNewProfileHandler),
    ("/profile.*", ViewProfileHandler),
    ('/img', Image),
    ('.*', PageNotFoundHandler),
], debug=True)
