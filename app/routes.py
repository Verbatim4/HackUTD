from app import app
from flask import render_template, request, redirect, url_for, session

from .utils.get_user_data import get_database_reference
from datetime import datetime

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
                'start-time': request.form['start-time'],
                'end-time': request.form['end-time'],
                'available-spots': request.form['available-spots'],
                'category': request.form['category'],
                'license-number': request.form['license-number'],
                'mileage': request.form['mileage'],
                'distance': request.form['distance'],
            }

            ref.push(data_packet)
            rides = ref.get()

        elif request.form.get('type') == 'filter':
            filter_date = request.form['date']
            time_range = request.form['time']
            category = request.form['category']

            rides_iterate = ref.get()  

            rides_date = set()
            for ride_key, ride_value in rides_iterate.items():
                if not filter_date:
                    rides_date.add(ride_key)
                    continue

                if filter_date == ride_value['date']:
                    rides_date.add(ride_key)
            
            am_10 = datetime.strptime("10:00", "%H:%M").time()
            pm_12 = datetime.strptime("12:00", "%H:%M").time()
            pm_02 = datetime.strptime("14:00", "%H:%M").time()
            pm_04 = datetime.strptime("16:00", "%H:%M").time()
            pm_06 = datetime.strptime("18:00", "%H:%M").time()
            pm_08 = datetime.strptime("20:00", "%H:%M").time()
            pm_10 = datetime.strptime("22:00", "%H:%M").time()
        
            rides_time = set()
            for ride_key, ride_value in rides_iterate.items():
                if not time_range:
                    rides_time.add(ride_key)
                    continue
                
                time_formatted = datetime.strptime(ride_value['start-time'], "%H:%M").time()

                if time_range == 'time-1':
                    if am_10 <= time_formatted < pm_12:
                        rides_time.add(ride_key)
                if time_range == 'time-2':
                    if pm_02 <= time_formatted < pm_04:
                        rides_time.add(ride_key)
                if time_range == 'time-3':
                    if pm_06 <= time_formatted < pm_08:
                        rides_time.add(ride_key)
                if time_range == 'time-4':
                    if pm_10 <= time_formatted:
                        rides_time.add(ride_key)

            rides_category = set()
            for ride_key, ride_value in rides_iterate.items():
                if not category:
                    rides_category.add(ride_key)
                    continue

                if ride_value['category'] == category:
                    rides_category.add(ride_key)

            print(rides_date, rides_time, rides_category)
            print('\n\n\n\n\n')
            rides_intersection = set.intersection(rides_date, rides_time, rides_category)

            rides = []

            for i, v in rides_iterate.items():
                for j in rides_intersection:
                    if i == j:
                        rides.append(v)
    
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