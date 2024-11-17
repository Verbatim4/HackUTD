from app import app
from flask import render_template, request, redirect, url_for, session

from .utils.get_user_data import get_database_reference
import datetime

@app.route('/', methods=('GET', 'POST'))
def index():
    if not session:
        if request.method == 'POST':
            ref = get_database_reference('/users')

            if request.form['type'] == 'sign-in':
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

                ref.push(user_packet)
            
            elif request.form['type'] == 'log-in':
                print('HELLO!')
                for i in ref.get():
                    print(i)

        else:
            return render_template('index.html', session=None)
            
        session['user_info'] = user_packet
        user_info = user_packet

    user_info = session['user_info']
    if user_info:
        return render_template('index.html', 
            f_name=user_info['f_name'], 
            l_name=user_info['l_name'], 
            email=user_info['email']
        )
    else:
        return render_template('index.html', session=None)

@app.route('/signout/')
def sign_out():
    session.clear()
    return redirect(url_for('index'))

@app.route('/signup/')
def sign_up():
    return render_template('signup.html')

@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/postride/', methods=('GET', 'POST'))
def postride():
    distance = None
    if request.method == 'POST':
        distance = request.form['distance']

    return render_template('postride.html', distance=distance)


@app.route('/home/')
def home():
    return render_template('index.html')

@app.route('/catalog/', methods=('GET', 'POST'))
def catalog():
    ref = get_database_reference('/ride_data')
    if request.method == 'POST':
        if request.form.get('type') == 'postride':

            data_packet = {
                'date': request.form['date'],
                'start_time': request.form['start-time'],
                'end-time': request.form['end-time'],
                'available-spots': request.form['available-spots'],
                'category': request.form['category'],
                'license-number': request.form['license-number'],
                'mileage': request.form['mileage'],
                'distance': request.form['distance'],
            }

            ref.push(data_packet)
        
        elif request.form.get('type') == 'filter':
            filter_date = request.form['date']
            time_range = request.form['time']
            category = request.form['category']

            rides_iterate = ref.get()  

            rides = []
            for ride in rides_iterate:
                if filter_date:
                    if filter_date == [i[0] for i in ride.values()][0]['date']:
                        rides.append(ride)
    
    else:
        rides = ref.get()

    return render_template('catalog.html', rides=rides)

@app.route('/ride/')
def ride():
    return render_template('ride.html')

@app.route('/map/')
def map():
    return render_template('maps.html')

@app.route('/info')
def info():
    return render_template('info.html')