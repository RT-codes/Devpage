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

class context:
    """
    This class is used to determine what the user has access to. 
     - If the user is authenticated then they can see the console and adminNav buttons
     - If the user is not authenticated then they will not have access to either of these buttons
    # example usage:
    contextObject = context( current_user )
    pageData = {
        'baseLayer' : "",
        'UserLayer' : contextObject.GetContext()
    }
    """
    def __init__(self, current_user = None):     
        self.current_user = current_user
        # create a list boolean to determine if the console panel should be displayed
        self.changes = []
 
        if current_user.is_authenticated:
            self.changes.append('console')
            self.changes.append('adminNav')
        else:
            self.current_user = None
        
    def GetContext(self):
        if(self.current_user != None):
            if self.current_user.is_authenticated:
                return self.changes
            else:
                return None
        else:
            return None

@app.route('/')
def index():
    return render_template( 'home.html' )

@app.route('/digital-garden')
def digital_garden():
    articles = Article.query.order_by(Article.creationdate.desc()).all()
    return render_template('digital-garden.html' , articles=articles)

@app.route('/article/<int:id>')
def article(id):
    article = Article.query.get(id)
    return render_template('article.html' , article=article )



# ------------------ LOGIN ------------------

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# logic routes
@app.route('/layers' , methods=['GET', 'POST'])
def layers():
    if request.method == 'GET':
        contextObject = context( current_user )
        pageData ={
            'baseLayer' : "",
            'UserLayer' : contextObject.GetContext()
        }
        return pageData
    return ""

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
                return redirect(url_for('admin_panel.html') ,)
            else:
                flash('Invalid username or password')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    print('user_id is being loaded')
    print(user_id)
    if user_id is not None:
        user_id = User.query.get(int(user_id))
    return user_id

# ------------------ CMS ------------------


@app.route('/admin-panel')
@login_required
def admin_panel():
    """ Render the admin panel for authenticated users. """
    articles = Article.query.order_by(Article.creationdate.desc()).all()
    return render_template('admin-panel.html' , articles=articles)


@app.route('/add-article', methods=['GET', 'POST'])
@login_required
def add_article():
    if request.method == 'POST':
        print(request.form)

        # if the debug checkbox key is not in the request.form dictionary, then it means that the checkbox was not checked
        if 'debug' not in request.form:
            article = Article(title=request.form['title'], textcontent=request.form['textcontent'], creationdate=datetime.utcnow())
            db.session.add(article)
            db.session.commit()
            flash('Article added successfully!')
            return redirect(url_for('index'))
        else:
            print('debug mode')
            print(request.form)
            return render_template('add-article.html')
    
    return render_template('add-article.html')

@app.route('/edit-article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    """ Edit an article from the database. """
    article = Article.query.get(id)
    return render_template('edit-article.html' , article=article )

@app.route('/delete-article/<int:id>')
@login_required
def delete_article(id):
    """ Delete an article from the database. """
    Article.query.filter_by(id=id).delete()
    db.session.commit()
    # flash('Article deleted successfully!')
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    print('running app from main.py function')
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
