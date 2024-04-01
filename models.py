from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

db= SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app=app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username= db.Column(db.String(20), nullable=False,unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name=db.Column(db.String(30), nullable=False)
    last_name=db.Column(db.String(20), nullable=False)
    favorites =db.relationship('Favorite',backref='users')
    votes =db.relationship('Vote',backref='users')
    
    @classmethod
    def register(cls,username,password,first_name,last_name):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user=cls(username=username,password=hashed_utf8,first_name=first_name,last_name=last_name)
        return user
    @classmethod
    def authenticate(cls,username,password):
        user=User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password,password):
            return user
        else:
            return False
        
class News(db.Model):
    __tablename__ = "news"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    author=db.Column(db.Text)
    title=db.Column(db.Text,nullable=False)
    description=db.Column(db.Text,nullable=False)
    url=db.Column(db.Text,nullable=False)
    image_url=db.Column(db.Text)
    publisedAt=db.Column(db.DateTime,nullable=False)
    content=db.Column(db.Text)
    favorite_news =db.relationship('Favorite',backref='news')
    

class Favorite(db.Model):
    __tablename__ = "favorites"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)
    news_id=db.Column(db.Integer, db.ForeignKey('news.id'),primary_key=True)

class Vote(db.Model):
    __tablename__ = "votes"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)
    news_id=db.Column(db.Integer, db.ForeignKey('news.id'),primary_key=True)
    
