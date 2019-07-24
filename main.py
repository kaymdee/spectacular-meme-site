#main.py
# the import section
import webapp2
import jinja2
import os
import time
from models import Post, Comment, User
from datetime import datetime
import google.appengine.
# from google.appengine.api.images import images
from google.appengine.api import users

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# the handler section
class MainPage(webapp2.RequestHandler):
    def get(self):
        gUser = users.get_current_user()
        #If user is logged in
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

        self.response.headers['Content-Type'] = 'html' #change this to write html!
        template = jinja_env.get_template('templates/index.html')
        dict = {
            "signoutHtml" : signoutHtml,
            "signInOrProfileHtml" : signInOrProfileHtml

        }

        self.response.write(template.render(dict))


class CreateNewProfileHandler(webapp2.RequestHandler):
    def get(self):
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
        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        template = jinja_env.get_template('templates/newPost.html')
        self.response.write(template.render())

        postTime = datetime.now()
        postTitle = self.request.get("post-title")
        postAuthor = self.request.get("post-author")
        postDescription = self.request.get("post-description")
        image = Post.get_by_id(int(self.request.get("post-image")))
        postImage = images.Image(image.fullSize)

        # image.resize(width = 150, height = 150)
        # seenImage = image.execute_transforms(output_encoding=images.JPEG)

        new_post_entity = Post(postTime, postAuthor, postDescription, postImage)
        new_post_entity.put()

class ShowPostPage(webapp2.RequestHandler):
    def get(self):
        pass
    def post(self): #for a post request from NewPostPage
        postTitle = self.request.get("post-title")
        postAuthor = self.request.get("post-author")
        postContent = self.request.get("post-content")
        postDate = str(time.asctime(time.localtime(time.time())))
        newBlogPostKey = models.Post(postTitle=postTitle, postAuthor=postAuthor,postContent=postContent).put()
        postDict = {#DASHES IN JINJA ARE FOR WHITESPACE CONTROL. NOT ALLOWED FOR JINJA VARIABLES
            "postTitle" : postTitle,
            "postAuthor" : postAuthor,
            "postContent" : postContent,
            "postDate" : postDate,
        }
        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        template = jinja_env.get_template('templates/showPost.html')
        self.response.write(template.render(postDict))

class ViewPostsPage(webapp2.RequestHandler):
    def get(self):
        blogPosts = models.Post.query().order(models.BlogPost.postTime).fetch()
        template = jinja_env.get_template("templates/viewPosts.html")
        self.response.write(template.render({"blogPosts":blogPosts}))

class ViewProfileHandler(webapp2.RequestHandler):
    def get(self):
        gUser = users.get_current_user()
        user = models.User.get_by_id(gUser.user_id())

        template = jinja_env.get_template("templates/profile.html")
        dict = {"firstName" : user.firstName,
                "lastName" : user.lastName,
                "email" : user.email}
        self.response.write(template.render(dict))
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
    ("/showPost.*",ShowPostPage),
    ("/viewPosts.*", ViewPostsPage),
    ("/createNewProfile.*", CreateNewProfileHandler),
    ("/profile.*", ViewProfileHandler),
    ('.*', PageNotFoundHandler),
], debug=True)
