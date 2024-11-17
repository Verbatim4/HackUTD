from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'money!!!'

from app import routes
from app.utils import *
