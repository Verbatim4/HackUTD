from app import app
from flask import render_template

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup')
def sign_up():
    return render_template('signup.html')

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')