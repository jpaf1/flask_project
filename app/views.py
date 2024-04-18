from app import app
from flask import request, Response
from app import USERS, POSTS, models
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

    if not models.User.validate_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

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

@app.post('/posts/create')
def post_create():
    data = request.get_json()
    id = len(POSTS)
    try:
        author_id = int(data["author_id"])
    except:
        return Response(status=HTTPStatus.BAD_REQUEST)
    text = data["text"]

    post = models.Post(id, author_id, text)
    for i in range(len(USERS)):
        if USERS[i].id == author_id:
            POSTS.append(post)
            USERS[i].posts.append(id)
            response = Response(
                json.dumps({
                    "id": post.id,
                    "author_id": post.author_id,
                    "text": post.text,
                    "reactions": post.reactions,
                }),
                200,
                mimetype="application/json",
            )
            return response
    return Response(status=HTTPStatus.BAD_REQUEST)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    if post_id < 0:
        return Response(status=HTTPStatus.NOT_FOUND)
    for i in range(len(POSTS)):
        if POSTS[i].id == post_id:
            response = Response(
                json.dumps({
                    "id": POSTS[i].id,
                    "author_id": POSTS[i].author_id,
                    "text": POSTS[i].text,
                    "reactions": POSTS[i].reactions,
                }),
                200,
                mimetype="application/json",
            )
            return response
    return Response(status=HTTPStatus.NOT_FOUND)

@app.post('/posts/<int:post_id>/reaction')
def post_reaction(post_id):
    data = request.get_json()
    try:
        user_id = int(data["user_id"])
    except:
        return Response(status=HTTPStatus.BAD_REQUEST)
    reaction = data["reaction"]
    for i in range(len(USERS)):
        if USERS[i].id == user_id:
            USERS[i].total_reactions += 1
            for i in range(len(POSTS)):
                if POSTS[i].id == post_id:
                    POSTS[i].reactions.append(reaction)
                    return Response(status=200)
    return Response(status=HTTPStatus.NOT_FOUND)