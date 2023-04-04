from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Article, User
import os

os.environ['FLASK_APP'] = 'main'


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:r84jEJX4qmwBLBk4kIFo@containers-us-west-26.railway.app:6403/railway'

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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
