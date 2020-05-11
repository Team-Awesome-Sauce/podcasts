from flask import Blueprint, jsonify, request, session
from sql_alchemy_db_instance import db
from models import Podcast, Users, PlaylistItems, Playlists, History
from hashutils import make_salt, make_pw_hash, check_pw_hash

users_api = Blueprint('users_api', __name__)


@users_api.route('/duplicate-user-test', methods=["POST"])
def test_duplicate_user():
    # return either a current user object (in the case that a username already exists),
    # or an empty array (if a username hasn't been taken yet)
    username = request.json["username"]
    username.lower()
    user_in_db = db.session.query(Users).filter(Users.username == username.lower()).all()
    user_in_db_results = [{"id": user.id, "user_username": user.username} for user in user_in_db]
    return jsonify({"does_the_user_exist": user_in_db_results})


@users_api.route('/add-user', methods=["POST"])
def add_user():
    print("hello?")
    # add a new user to the User Table in DB
    new_user = Users()
    new_user.username = request.json["username"]
    plain_text_password = request.json["password"]
    salt = make_salt()
    # save unique salts in the db with each user
    new_user.salt = salt
    # salt and hash all passwords being entered into db
    new_user.password = make_pw_hash(salt, plain_text_password)
    db.session.add(new_user)
    db.session.commit()
    # add the user to session
    session['user'] = new_user.username
    return jsonify({"username": new_user.username})


@users_api.route('/login', methods=["POST"])
def login():
    username = request.json['username']
    username.lower()
    password = request.json['password']
    # query the database with the provided username
    user = Users.query.filter_by(username=username.lower()).one_or_none()
    # if the response is 'None', the username entered isn't valid
    if user == None:
        return 'None'
    if check_pw_hash(user.salt, password, user.password):
        # if the username was valid and the password entered matches the password
        # in the DB, create a session for that user
        session['user'] = user.username
        return jsonify({"username": user.username})
    return jsonify(success=False)


@users_api.route('/users', methods=['POST', 'GET'])
def test_users_in_session():
    # test if there's currently a user in session -
    # the response of this function is what the navbar is referencing
    # in order to determine which buttons to display
    if 'user' in session:
        return jsonify({"userInSession": session['user']})
    return jsonify(success=False)


@users_api.route('/logout', methods=['POST', 'GET'])
def logout():
    # delete a user's session, logging them out
    del session['user']
    return jsonify(success=True)
