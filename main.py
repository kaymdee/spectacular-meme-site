#main.py
# the import section
import webapp2
import jinja2
import os
import time
import models
the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# the handler section
class MainPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        story_template = the_jinja_env.get_template('templates/index.html')
        self.response.write(story_template.render())



class FroggerPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        story_template = the_jinja_env.get_template('templates/frogger.html')
        self.response.write(story_template.render())

class PongPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        story_template = the_jinja_env.get_template('templates/pong.html')
        self.response.write(story_template.render())

class RPSPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        story_template = the_jinja_env.get_template('templates/RPS.html')
        self.response.write(story_template.render())
class NewPostPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        template = the_jinja_env.get_template('templates/newPost.html')
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
        template = the_jinja_env.get_template('templates/showPost.html')
        self.response.write(template.render(postDict))

class ViewPostsPage(webapp2.RequestHandler):
    def get(self):
        blogPosts = models.BlogPost.query().order(models.BlogPost.postTime).fetch()
        template = the_jinja_env.get_template("templates/viewPosts.html")
        self.response.write(template.render({"blogPosts":blogPosts}))


class PageNotFoundHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html' #change this to write html!
        no_page_template = the_jinja_env.get_template("templates/pagenotfound.html")
        self.response.write(no_page_template.render())
# the app configuration section
app = webapp2.WSGIApplication([
    ("/", MainPage),
    ('/index.*', MainPage), #this maps the root url to the Main Page Handler
    ('/frogger.*', FroggerPage),
    ('/pong.*', PongPage),
    ('/RPS.*', RPSPage),
    ("/newPost.*", NewPostPage),
    ("/showPost.*",ShowPostPage),
    ("/viewPosts.*", ViewPostsPage),
    ('.*', PageNotFoundHandler),
], debug=True)
