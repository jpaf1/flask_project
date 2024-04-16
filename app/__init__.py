from flask import Flask

app = Flask(__name__)

USERS = [] #list for objects of type user

from app import views
from app import models
