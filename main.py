import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# we'll use this template in a few different places
t_scaffolding = jinja_env.get_template("scaffolding.html")

# a list of movies that nobody should be allowed to watch
terrible_movie_titles = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives"
]

# create a Movie class
class Movie(db.Model):
    title = db.StringProperty(required = True)
    watched = db.BooleanProperty(required = True, default = False)
    rating = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True)


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """

    def get(self):
        unwatched_movies = db.GqlQuery("SELECT * FROM Movie WHERE watched = False")

        t_frontpage = jinja_env.get_template("frontpage.html")
        frontpage_content = t_frontpage.render(
                                movies = unwatched_movies,
                                error = self.request.get("error"))

        response = t_scaffolding.render(
                    title = "FlickList: My Watchlist",
                    content = frontpage_content)
        self.response.write(response)


class AddMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/add'
        e.g. www.flicklist.com/add
    """

    def post(self):
        new_movie = self.request.get("new-movie")
        print("the new movie is " + new_movie)

        # if the user typed nothing at all, redirect and yell at them
        if (not new_movie) or (new_movie.strip() == ""):
            print("We caught the error")
            error = "Please specify the movie you want to add."
            self.redirect("/?error=" + cgi.escape(error))
            return

        # if the user wants to add a terrible movie, redirect and yell at them
        if new_movie in terrible_movie_titles:
            error = "Trust me, you don't want to add '{0}' to your Watchlist.".format(new_movie)
            self.redirect("/?error=" + cgi.escape(error, quote = True))
            return

        # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
        new_movie_escaped = cgi.escape(new_movie, quote = True)

        # add the new movie to the database
        movie_obj = Movie(title = new_movie_escaped, watched = False)
        movie_obj.put()

        # redirect back to homepage
        self.redirect("/")


class WatchedMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/watched-it'
        e.g. www.flicklist.com/watched-it
    """

    def post(self):
        movie_id = self.request.get("movie")

        # if the movie id is nonexistant, reject.
        if not movie_id:
            error = "Please specify a movie to watch."
            self.redirect("/?error=", cgi.escape(error))
            return

        # get the movie with the matching id
        movie = Movie.get_by_id(int(movie_id))

        # if user tried to cross off a movie that is not in their list, reject
        if movie == None:
            error_escaped = cgi.escape("Invalid movie to watch " + movie_id, quote=True)

            # redirect to homepage, and include error as a query parameter in the URL
            self.redirect("/?error=" + error_escaped)
            return

        # set `watched` to True and save to the database
        movie.watched = True
        movie.put()

        # redirect to the ratings page
        self.redirect("/ratings")


class MovieRatings(webapp2.RequestHandler):
    """ Handles requests coming in to '/ratings'
        e.g. www.flicklist.com/ratings
    """

    def get(self):
        # get all the movies that the user has watched
        watched_movies = db.GqlQuery("SELECT * FROM Movie WHERE watched = True ORDER BY created desc")

        t_ratings = jinja_env.get_template("ratings.html")
        ratings_content = t_ratings.render(movies = watched_movies)
        response = t_scaffolding.render(content = ratings_content)
        self.response.write(response)

    def post(self):
        # get the movie
        movie_id = self.request.get("movie-id")
        movie = Movie.get_by_id( int(movie_id) )

        # get the rating
        new_rating = self.request.get("rating")

        # if they both exist, update the movie's rating
        if movie and new_rating:
            movie.rating = new_rating
            print ("attempted rating is " + new_rating)
            print("new rating is " + movie.rating)
            movie.put()

        self.redirect("/ratings")


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/ratings', MovieRatings),
    ('/add', AddMovie),
    ('/watched-it', WatchedMovie),
], debug=True)


# create unwatched view
    # create watchlist template, render it in Index

# create Movie class
    # fix templates to use movie.title
    # fix cross-off validation (can't compare string to object, look at movie.title property)
