import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# load some templates
t_scaffolding = jinja_env.get_template("scaffolding.html")

# a list of movies that nobody should be allowed to watch
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives"
]


# create a Movie class
class Movie(db.Model):
    title = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


def getCurrentWatchlist():
    """ Returns the user's current watchlist """

    return [
        # now let's use Movie objects instead of just strings
        Movie(title="Star Wars"),
        Movie(title="Minions"),
        Movie(title="Freaky Friday"),
        Movie(title="My Favorite Martian")
    ]


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """

    def get(self):
        # add watchlist content to the response
        t_watchlist = jinja_env.get_template("watchlist.html")
        watchlist_content = t_watchlist.render(
                        watchlist = getCurrentWatchlist(),
                        error = self.request.get("error"))
        t_edit = jinja_env.get_template("edit.html")
        edit_content = t_edit.render(
                        watchlist = getCurrentWatchlist(),
                        error = self.request.get("error"))
        response = t_scaffolding.render(
                    title = "FlickList: My Watchlist",
                    content = watchlist_content + edit_content)
        self.response.write(response)


class AddMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/add'
        e.g. www.flicklist.com/add
    """

    def post(self):
        new_movie = self.request.get("new-movie")

        # if the user typed nothing at all, redirect and yell at them
        if (not new_movie) or (new_movie.strip() == ""):
            error = "Please specify the movie you want to add."
            self.redirect("/?error=" + cgi.escape(error))

        # if the user wants to add a terrible movie, redirect and yell at them
        if new_movie in terrible_movies:
            error = "Trust me, you don't want to add '{0}' to your Watchlist.".format(new_movie)
            self.redirect("/?error=" + cgi.escape(error, quote = True))

        # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
        new_movie_escaped = cgi.escape(new_movie, quote = True)

        # render the confirmation message
        t_add = jinja_env.get_template("add.html")
        add_content = t_add.render(movie = new_movie_escaped)
        response = t_scaffolding.render(
                        title = "FlickList: Add a Movie",
                        content = add_content)
        self.response.write(response)


class CrossOffMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/cross-off'
        e.g. www.flicklist.com/cross-off
    """

    def post(self):
        crossed_off_movie = self.request.get("crossed-off-movie")

        # if the movie movie is just whitespace (or nonexistant), reject.
        # (we didn't check for this last time--only checked in the AddMovie handler--but we probably should have!)
        if not crossed_off_movie or crossed_off_movie.strip() == "":
            error = "Please specify a movie to cross off."
            self.redirect("/?error=", cgi.escape(error))

        # if user tried to cross off a movie that is not in their list, reject
        watchlist_movies_with_same_title = [
            movie for movie in getCurrentWatchlist() if movie.title == crossed_off_movie
        ]
        if len(watchlist_movies_with_same_title) == 0:
            # make a helpful error message
            error = "'{0}' is not in your Watchlist, ".format(crossed_off_movie)
            error += "so you can't cross it off!"
            error_escaped = cgi.escape(error, quote=True)

            # redirect to homepage, and include error as a query parameter in the URL
            self.redirect("/?error=" + error_escaped)

        # render confirmation page
        t_cross_off = jinja_env.get_template("cross-off.html")
        cross_off_content = t_cross_off.render(movie=crossed_off_movie)
        response = t_scaffolding.render(
                    title = "FlickList: Cross a Movie Off",
                    content = cross_off_content)
        self.response.write(response)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', AddMovie),
    ('/cross-off', CrossOffMovie)
], debug=True)


# create watchlist view
    # create watchlist template, render it in Index

# create Movie class
    # fix templates to use movie.title
    # fix cross-off validation (can't compare string to object, look at movie.title property)
