from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from models import db, Article, User
import os
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_login import login_required , LoginManager , current_user , login_user , logout_user

os.environ['FLASK_APP'] = 'main'


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:r84jEJX4qmwBLBk4kIFo@containers-us-west-26.railway.app:6403/railway'

# generate a random key
random_key = os.urandom(24)
app.secret_key = random_key
app.config['WTF_CSRF_SECRET_KEY'] = 'random_key'

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template( 'home.html' )

@app.route('/articles')
def articles():
    articles = Article.query.all()
    return render_template( 'articles.html', articles=articles )

# ------------------ LOGIN ------------------

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        print(request.form)
        if form.validate_on_submit():
            print('form validated')
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                session['user_id'] = user.id
                login_user(user)
                print(f"user {username} logged in successfully")
                return redirect(url_for('admin_panel') ,)
            else:
                flash('Invalid username or password')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

# ------------------ CMS ------------------


if __name__ == '__main__':
    print('running app from main.py function')
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
