from app import app
from flask import render_template, request, redirect, url_for, session

from .utils.get_user_data import get_database_reference

@app.route('/', methods=('GET', 'POST'))
def index():
    if not session:
        if request.method == 'POST':
            email = request.form['floating_email']
            password = request.form['floating_password']
            repeat_password = request.form['repeat_password']
            f_name = request.form['floating_first_name']
            l_name = request.form['floating_last_name']

            if password != repeat_password:
                    return redirect(url_for('sign_up'))

            user_packet = {
                'f_name': f_name,
                'l_name': l_name,
                'email': email,
                'password': password,
            }

            ref = get_database_reference('/users')
            ref.push(user_packet)

            print('put user in db')

        else:
            print('returned null session site')
            return render_template('index.html', session=None)
            
        session['user_info'] = user_packet
        print('site with new session info')
        return render_template('index.html', 
            f_name=user_info['f_name'], 
            l_name=user_info['l_name'], 
            email=user_info['email']
        )
    
    else:
        print(session)
        user_info = session['user_info']
        return render_template('index.html', 
            f_name=user_info['f_name'], 
            l_name=user_info['l_name'], 
            email=user_info['email']
        )

@app.route('/signup/')
def sign_up():
    return render_template('signup.html')

@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/postride/')
def postride():
    return render_template('postride.html')


@app.route('/home/')
def home():
    return render_template('index.html')

@app.route('/catalog/')
def catalog():
    return render_template('catalog.html')

@app.route('/ride/')
def ride():
    return render_template('ride.html')

@app.route('/map/')
def map():
    return render_template('maps.html')

@app.route('/info')
def info():
    return render_template('info.html')