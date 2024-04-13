import os

from flask import Flask, render_template, request,redirect, session,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, News, Favorite, Vote
from forms import UserForm, LoginForm
import requests


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///everyday-news')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']='everyday-news'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

debug= DebugToolbarExtension(app)
connect_db(app)

@app.route('/')
def home_page():
    is_sorted = request.args.get('sorted')
    if not is_sorted:
        is_sorted = False
    news_list = []
    if is_sorted:
        votes = Vote.query.with_entities(Vote.news_id, db.func.count(Vote.news_id)).group_by("news_id").order_by(db.func.count(Vote.news_id).desc()).all()
        for vote in votes:
            news = News.query.filter_by(id=vote.news_id).first()
            news_list.append(news)
    else:
        news_list= News.query.all()
    return render_template('home.html',news=news_list)

@app.route('/sign-up',methods=["GET","POST"])
def sign_up():
    form=UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password=form.password.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        new_user=User.register(username,password,first_name,last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username']=new_user.username
        return redirect(f"/users/{new_user.username}")
    return render_template('sign_up.html',form=form)

@app.route('/users/<username>')
def show_user(username):
    if 'username' not in session:
        flash('login first to see your account..')
        return redirect('/login')
    user = User.query.filter_by(username=username).first()
    is_sorted = request.args.get('sorted')
    if not is_sorted:
        is_sorted = False
    news_list = []
    if is_sorted:
        votes = Vote.query.with_entities(Vote.news_id, db.func.count(Vote.news_id)).group_by("news_id").order_by(db.func.count(Vote.news_id).desc()).all()
        for vote in votes:
            news = News.query.filter_by(id=vote.news_id).first()
            news_list.append(news)
    else:
        news_list= News.query.all()
    return render_template('user.html',user=user,news=news_list)

@app.route('/login',methods=["GET","POST"])
def log_in():
    form =LoginForm()
    if form.validate_on_submit():
        username =form.username.data
        password =form.password.data
        user = User.authenticate(username,password)
        if user:
            flash(f"Welcome  {user.username}!!")
            session['username'] =user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_user():
    del session['username']
    return redirect('/login')

@app.route('/refresh-news')
def get_data():
    apikey='xyz'

    response = requests.get(
        'https://newsapi.org/v2/top-headlines', 
        params={"apiKey":apikey, "country":'us'} 
        )
    json_response = response.json()
    print(json_response)
    articles = json_response['articles']
    for i in range(len(articles)):    
        author=articles[i]["author"]
        title=articles[i]["title"]
        description=articles[i]["description"]
        url=articles[i]["url"]
        image_url=articles[i]["urlToImage"]
        publisedAt=articles[i]["publishedAt"]
        content=articles[i]["content"]
        if title and description and url and publisedAt and not News.query.filter_by(url=url).first():
            new_news=News(author=author,title=title,description=description,url=url,image_url=image_url,publisedAt=publisedAt,content=content)
            db.session.add(new_news)

    db.session.commit()
    return redirect('/')

@app.route('/users/<username>/favorites')
def user_favorites(username):
    user=User.query.filter_by(username=username).first()
    favorites = user.favorites
    favorite_news = []
    for favorite in favorites:
        favorite_news.append(favorite.news)
    return render_template('user_favorite.html',favorite_news=favorite_news,user=user)

@app.route('/users/<username>/new-favorite',methods=["POST"])
def user_new_favorite(username):
    news_id = int(request.form["newsid"])
    user=User.query.filter_by(username=username).first()
    user_id = user.id 
    favorites = user.favorites
    favorite_news_ids = []
    for favorite in favorites:
        favorite_news_ids.append(favorite.news_id)
    if news_id not in favorite_news_ids:       
        new_favorite=Favorite(user_id=user_id,news_id=news_id)
        db.session.add(new_favorite)
        db.session.commit()
    return redirect(f"/users/{user.username}/favorites")

@app.route('/users/<username>/vote',methods=["POST"])
def user_vote(username):
    news_id = int(request.form["newsid"])
    user=User.query.filter_by(username=username).first()
    user_id = user.id 
    user_votes=user.votes
    vote_news=[]
    for vote in user_votes:
        vote_news.append(vote.news_id)  
    if news_id not in vote_news:     
        user_vote=Vote(user_id=user_id,news_id=news_id)
        db.session.add(user_vote)
        db.session.commit()
    return redirect(f"/users/{user.username}")
    




