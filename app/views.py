from app import app
from flask import request, Response
from app import USERS, POSTS, models
import json
from http import HTTPStatus
import matplotlib.pyplot as plt

plt.rc('xtick', labelsize=8)
GRAPH = plt.subplot()

@app.route('/')
def index():
    return "<h1>Hello world<h1>"

@app.route('/test')
def test():
    graph = plt.subplot()
    users = []
    reactions = []
    graph.bar(users, reactions)
    graph.set_ylabel("User reaction")
    graph.set_title("User leaderboard by score")
    plt.savefig("leaderboard_graph.png")


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
        mimetype="application/json",
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


@app.route('/users/leaderboard')
def leaderboard():
    data = request.get_json()
    type = data["type"]

    leaderboard = USERS
    for i in range(len(leaderboard) - 1):
        for j in range(i + 1, len(leaderboard)):
            if leaderboard[i] < leaderboard[j]:
                container = leaderboard[i]
                leaderboard[i] = leaderboard[j]
                leaderboard[j] = container
    if type == "list":
        sort = data["sort"]
        leaderboard_list = []
        for i in range(len(leaderboard)):
            leaderboard_list.append({
                "id": leaderboard[i].id,
                "first_name": leaderboard[i].first_name,
                "last_name": leaderboard[i].last_name,
                "email": leaderboard[i].email,
                "total_reactions": leaderboard[i].total_reactions,
            })
        if sort == "desc":
            response = Response(
                json.dumps({
                    "leaderboard": leaderboard_list
                }),
                200,
                mimetype="application/json",
            )
            return response

        if sort == "asc":
            response = Response(
                json.dumps({
                    "leaderboard": leaderboard_list[::-1]
                }),
                200,
                mimetype="application/json",
            )
            return response
    if type == "graph":
        users = []
        reactions = []
        for i in range(len(leaderboard)):
            users.append(f"{leaderboard[i].first_name} {leaderboard[i].last_name} ({leaderboard[i].id})")
            reactions.append(leaderboard[i].total_reactions)
        GRAPH.bar(users, reactions)
        GRAPH.set_ylabel("User reaction")
        GRAPH.set_title("User leaderboard by score")
        plt.savefig("app/static/leaderboard_graph.png")
        return Response('<img src="/static/leaderboard_graph.png">',
                        status=200,
                        mimetype="text/html",
                        )
