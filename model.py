"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Movie(db.Model):
    """Movie on ratings website."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64))
    released_at = db.Column(db.DateTime)
    imdb_url = db.Column(db.String(200))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Movie movie_id=%s title=%s>" % (self.movie_id, self.title)


class Rating(db.Model):
    """Rating of a movie by a user."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("ratings", order_by=rating_id))

    # Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
            self.rating_id, self.movie_id, self.user_id, self.score)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."

    # 1. find the user with the email cats@gmail.com #######################
    User.query.filter(User.email == "cats@gmail.com").one()
    # alternative solution, returns all if more than one user has same email
    User.query.filter(User.email == "cats@gmail.com").all()


    # 2. find any movies with the exact title "Cape Fear" ##################
    Movie.query.filter(Movie.title == "Cape Fear").all()


    # 3. Find all users with the zipcode 90703 #############################
    User.query.filter(User.zipcode == "90703").all()


    # 4. Find all ratings with score = 5 ###################################
    Rating.query.filter_by(rating_id = 5).all()


    # 5. Find the rating for the movie whose id is 7 #######################
    #    from the user whose id is 6
    Rating.query.filter(Rating.movie_id == 7, Rating.user_id == 6).all()


    # 6. Find all ratings that are larger than 3 ###########################
    Rating.query.filter(Rating.score > 3).all()
    