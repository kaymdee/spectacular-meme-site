#main.py
# the import section
import webapp2
import jinja2
import os
import time
import models
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
            signoutLinkHtml = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
            #user object exists already in data base
            if user:
                #Stuff
            #User has not been to our site
            else:

        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        template = jinja_env.get_template('templates/index.html')
        self.response.write(template.render())


class LogInHandler(webapp2.RequestHandler):#TODO NEEDS FIXING
  def get(self):
    gUser = users.get_current_user()
    # If the user is logged in...
    if gUser:
      email_address = gUser.nickname()
      user = models.User.get_by_id(gUser.user_id())
      signout_link_html = '<a href="%s">sign out</a>' % (
          users.create_logout_url('/'))
      # If the user has previously been to our site, we greet them!
      if user:
        self.response.write('''
            Welcome %s %s (%s)! <br> %s <br>''' % (
              user.firstName,
              user.lastName,
              email_address,
              signout_link_html))
      # If the user hasn't been to our site, we ask them to sign up
      else:
        self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/login">
            <input type="text" name="firstName">
            <input type="text" name="lastName">
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, signout_link_html))
    # Otherwise, the user isn't logged in!
    else:
      self.response.write('''
        Please log in to use our site! <br>
        <a href="%s">Sign in</a>''' % (
          users.create_login_url('/')))

  def post(self): #only when new account made
    gUser = users.get_current_user()
    if not gUser:
      # You shouldn't be able to get here without being logged in
      webapp2.redirect("/login")
      return
    user = models.User(
        firstName=self.request.get('firstName'),
        lastName=self.request.get('lastName'),
        email = gUser.nickname(),
        id=gUser.user_id())
    user.put()
    self.response.write('Thanks for signing up, %s!' %
        user.firstName)


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
class ShowPostPage(webapp2.RequestHandler):
    def get(self):
        pass
    def post(self): #for a post request from NewPostPage
        postTitle = self.request.get("post-title")
        postAuthor = self.request.get("post-author")
        postContent = self.request.get("post-content")
        postDate = str(time.asctime(time.localtime(time.time())))
        newBlogPostKey = models.BlogPost(postTitle=postTitle, postAuthor=postAuthor,postContent=postContent).put()
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
    ("/login.*", LogInHandler),
    ('.*', PageNotFoundHandler),
], debug=True)
