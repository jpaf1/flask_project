from app import app
from flask import request, Response
from app import USERS, models
import json
from http import HTTPStatus

@app.route('/')
def index():
    return "<h1>Hello world<h1>"


@app.post('/users/create')
def user_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    # todo check email

    user = models.User(id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "total_reactions": user.total_reactions,
            "posts": user.posts,
        }),
        200,
        mimetype = "application/json",
    )
    return response

@app.route('/users/<int:user_id>')
def show_user(user_id):
    if user_id < 0:
        return Response(status=HTTPStatus.NOT_FOUND)
    for i in range(len(USERS)):
        if USERS[i].id == user_id:
            response = Response(
                json.dumps({
                    "id": USERS[i].id,
                    "first_name": USERS[i].first_name,
                    "last_name": USERS[i].last_name,
                    "email": USERS[i].email,
                    "total_reactions": USERS[i].total_reactions,
                    "posts": USERS[i].posts,
                }),
                200,
                mimetype="application/json",
            )
            return response
    return Response(status=HTTPStatus.NOT_FOUND)