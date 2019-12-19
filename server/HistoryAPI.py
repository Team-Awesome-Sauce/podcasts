from flask import Blueprint, jsonify, request, session
from sql_alchemy_db_instance import db
from models import Podcast, Users, PlaylistItems, Playlists, History
from usersAPI import test_users_in_session
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from datetime import datetime

history_api = Blueprint('history_api', __name__)

@history_api.route('/duplicate-history-entry-test', methods=["POST"])
def test_duplicate_history_entry():
    # return either a current user object (in the case that a username already exists),
    # or an empty array (if a username hasn't been taken yet)
    episode_title = request.json["episode_title"]
    user = session['user']
    user_in_session = db.session.query(Users).filter(Users.username == user).first()
    user_id_of_user_in_session = user_in_session.id
    history_entry_in_db = db.session.query(History).filter(History.episode_title == episode_title).filter(History.user_id == user_id_of_user_in_session).all()
    history_entry_in_db_results = [{"id": history.id, "history_entry": history.episode_title} for history in history_entry_in_db]
    return jsonify({"does_the_history_entry_exist": history_entry_in_db_results})


@history_api.route('/my-history', methods=['GET'])
def show_my_history():
    user = session.get('user')
    user_in_session = db.session.query(Users).filter(Users.username == user).first()
    user_id_of_user_in_session = user_in_session.id
    my_history_instances = db.session.query(History).filter(History.user_id == user_id_of_user_in_session).all()
    podcast_items_in_history = [{"id": history.id, "user_id": history.user_id, "episode_title": history.episode_title, 
        "episode_summary": history.episode_summary, "episode_url": history.episode_url,"time_stamp_accessed": history.time_stamp_accessed, "current_time_listened": history.current_time_listened,
        "parent_podcast_id": history.parent_podcast_id, "parent_podcast_art_url": history.parent_podcast_art_url} for history in my_history_instances]
    return jsonify({"my_history_list": podcast_items_in_history})


@history_api.route('/add-to-history', methods=['POST'])
def add_to_history():
    new_history_item = History()
    user_in_session = session['user']
    username = db.session.query(Users).filter(Users.username == user_in_session).first()
    new_history_item.episode_summary = request.json['episode_summary']
    new_history_item.episode_url = request.json['episode_url']
    new_history_item.episode_title = request.json['episode_title'] 
    new_history_item.parent_podcast_id = request.json['parent_podcast_id']
    new_history_item.user_id = username.id
    new_history_item.current_time_listened = request.json['current_time_listened']
    new_history_item.episode_id = request.json['episode_title']
    new_history_item.parent_podcast_art_url = request.json['parent_podcast_art_url']
    date_obj = datetime.strptime(request.json["time_date"], "%Y-%m-%d %H:%M:%S")
    new_history_item.time_stamp_accessed = date_obj
    db.session.add(new_history_item)
    db.session.commit()
    return jsonify(success=True)

@history_api.route('/patch-current-time', methods=['PATCH'])
def patch_current_time_listened():
    episode_title = request.json["episode_title"]
    current_time = request.json["current_time"]
    user = session['user']
    user_in_session = db.session.query(Users).filter(Users.username == user).first()
    user_id_of_user_in_session = user_in_session.id
    history_entry_in_db = db.session.query(History).filter(History.episode_title == episode_title).filter(History.user_id == user_id_of_user_in_session).first()
    history_entry_in_db.current_time_listened = current_time
    db.session.commit()
    return jsonify(success=True)