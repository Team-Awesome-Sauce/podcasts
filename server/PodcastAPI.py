from flask import Blueprint, jsonify, request, session
from sql_alchemy_db_instance import db
from models import Podcast, Users, PlaylistItems, Playlists, History
import requests
from sqlalchemy import func

podcast_api = Blueprint('podcast_api', __name__)

@podcast_api.route('/check-if-subscribed', methods=['GET'])
def check_if_user_is_subscribed():
    #podcast_id = request.json["podcast_id"]
    #print("----------->", podcast_API_id)
    user_in_session_username = session['user']
    user_in_session_db_info = db.session.query(Users).filter(Users.username == user_in_session_username).first()
    user_id = user_in_session_db_info.id
    podcast_ids_instances = db.session.query(Podcast).filter(Podcast.user_id == user_id).filter(Podcast.podcast_API_id == podcast_id).all()
    podcast_API_ids_list = [ {"id": podcast.id, "podcast_API_id": podcast.podcast_API_id} for pod_ids in podcast_ids_instances]
    return jsonify ({"podcast_API_ids": podcast_API_ids_list})

@podcast_api.route('/subscriptions', methods=['GET'])
def serve_all_subscriptions():
    user_in_session_username = session['user']
    user_in_session_db_info = db.session.query(Users).filter(Users.username == user_in_session_username).first()
    user_id = user_in_session_db_info.id
    podcast_instances = db.session.query(Podcast).filter(Podcast.user_id == user_id).all()
    podcast_items = [{"id": podcast.id, "name": podcast.name, "rss_feed_url": podcast.rss_feed_url, "podcast_id": podcast.podcast_API_id} for podcast in podcast_instances]
    return jsonify({"name": podcast_items})


@podcast_api.route('/subscription', methods=['POST'])
def add_subscription():
    new_podcast = Podcast()
    user_in_session = session['user']
    username = db.session.query(Users).filter(Users.username==user_in_session).first()
    new_podcast.user_id = username.id
    new_podcast.podcast_API_id = request.json["podcast_id"]
    new_podcast.name = request.json["name"]
    new_podcast.rss_feed_url = request.json["rss_feed_url"]
    db.session.add(new_podcast)
    db.session.commit()
    return jsonify(success=True)


@podcast_api.route('/subscription', methods=['PATCH'])
# this is going to require an update - this is currently deleting the first instance of 
# a subscription to a particular podcast rather than the subscription instance relative to the proper user_id
def remove_subscription():
    pod_id = request.json["id"]
    target_podcast = db.session.query(Podcast).filter_by(id=pod_id).first()
    db.session.delete(target_podcast)
    db.session.commit()
    return jsonify(success=True)

# The request to the iTunes API to get the RSS feed is made here because of an error with some podcasts returning html instead of XML. Here we can set the Headers so that we only get an XMLHttpRequest reponse, which is what we need in order for the rss-parser library to parse the response in Podcast.vue.
@podcast_api.route('/itunes-api', methods=['POST'])
def get_feed():
    rss_feed = request.json["rss_feed"]
    podcast_info = requests.get("https://cors-anywhere.herokuapp.com/" + rss_feed, headers={"X-Requested-With": "XMLHttpRequest"})
    return podcast_info.content
