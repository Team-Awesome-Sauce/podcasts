from sql_alchemy_db_instance import db
from sqlalchemy import ForeignKey

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(128, nullable=False))
    salt = db.Column(db.String(40), nullable=False)

class Podcasts(db.Model):
    # we want to change the name of this table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2000))
    rss_url = db.Column(db.String(2000), nullable=False)

class Playlists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class PlaylistItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.id"))
    podcast_API_id = db.Column(db.Integer)
    episode_id = db.Column(db.Integer)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    episode_id = db.Column(db.Integer)
