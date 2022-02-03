from app import app
from .forms import EntryForm, LoginForm, RegisterForm
from flask import render_template, request, flash, redirect, url_for
import requests
from .models import User
from flask_login import current_user, logout_user, login_required, login_user

# Routes

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        email = request.form.get('email').lower()
        password = request.form.get('password')
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('Welcome to Fakebook', "success")
            return redirect(url_for('index')) #good login
        flash('Incorrect email password combo', "danager")
        return render_template('login.html.j2', form=form) #bad login
    return render_template('login.html.j2', form=form) #get request

@app.route('/logout')
# @login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out','warning')
        return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            flash('There was an unexpected error creating your account. Please try again.', 'danger')
            return render_template('register.html.j2', form=form)
        # if it works
        flash('You have registered successfully', 'success')
        return redirect(url_for('login'))
    # get return
    return render_template('register.html.j2', form=form)

@app.route('/entry', methods = ['GET', 'POST'])
# @login_required
def entry():
    form = EntryForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form.get('name').lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)
        if response.ok:
            pokemon_dict={
                "name":response.json()['forms'][0]['name'],
                "ability":response.json()['abilities'][0]['ability']['name'],
                "hp":response.json()['stats'][0]['base_stat'],
                "attack":response.json()['stats'][1]['base_stat'],
                "defense":response.json()['stats'][2]['base_stat'],
                "sprite": response.json()['sprites']['front_shiny']
                }
            return render_template('entry.html.j2', form=form, pokemon = pokemon_dict)

        else:
            error_string = f"{name} does not exist. Please try again."
            return render_template('entry.html.j2', form=form, error = error_string)
 
    else: # if its a get request
        return render_template('entry.html.j2', form=form)