from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Article, User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:r84jEJX4qmwBLBk4kIFo@containers-us-west-26.railway.app:6403/railway'

db.init_app(app)

@app.route('/')
def index():
    return render_template( 'home.html' )

@app.route('/articles')
def articles():
    articles = Article.query.all()
    return render_template( 'articles.html', articles=articles )

if __name__ == '__main__':
    app.run(port=5000)
