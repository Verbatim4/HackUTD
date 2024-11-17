from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup')
def sign_up():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/postride')
def postride():
    return render_template('post_ride.html')


@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/ride')
def ride():
    return render_template('ride.html')

@app.route('/map')
def map():
    return render_template('maps.html')